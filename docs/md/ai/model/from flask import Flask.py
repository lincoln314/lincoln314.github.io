from flask import Flask
from flask import jsonify
from flask import request

import scipy, cv2, os, sys, argparse, audio
import onnxruntime

from os import listdir, path
import numpy as np
import scipy, cv2, os, sys, argparse, audio
import json, subprocess, random, string
from tqdm import tqdm
from glob import glob
import torch, face_detection
import platform

import time

from cacheout import Cache
cache = Cache()


# 创建对象
app = Flask(__name__)


parser = argparse.ArgumentParser(description='Inference code to lip-sync videos in the wild using Wav2Lip models')

parser.add_argument('--checkpoint_path', type=str, 
					help='Name of saved checkpoint to load weights from', required=False)

parser.add_argument('--face', type=str, 
					help='Filepath of video/image that contains faces to use', required=False)
parser.add_argument('--audio', type=str, 
					help='Filepath of video/audio file to use as raw audio source', required=False)
parser.add_argument('--outfile', type=str, help='Video path to save result. See default for an e.g.', 
								default='results/result_voice.mp4')

parser.add_argument('--static', type=bool, 
					help='If True, then use only first video frame for inference', default=False)
parser.add_argument('--fps', type=float, help='Can be specified only if input is a static image (default: 25)', 
					default=25., required=False)

parser.add_argument('--pads', nargs='+', type=int, default=[0, 10, 0, 0], 
					help='Padding (top, bottom, left, right). Please adjust to include chin at least')

parser.add_argument('--face_det_batch_size', type=int, 
					help='Batch size for face detection', default=16)
parser.add_argument('--wav2lip_batch_size', type=int, help='Batch size for Wav2Lip model(s)', default=256)

parser.add_argument('--resize_factor', default=1, type=int, 
			help='Reduce the resolution by this factor. Sometimes, best results are obtained at 480p or 720p')

parser.add_argument('--crop', nargs='+', type=int, default=[0, -1, 0, -1], 
					help='Crop video to a smaller region (top, bottom, left, right). Applied after resize_factor and rotate arg. ' 
					'Useful if multiple face present. -1 implies the value will be auto-inferred based on height, width')

parser.add_argument('--box', nargs='+', type=int, default=[103, 301, 864, 1008], 
					help='Specify a constant bounding box for the face. Use only as a last resort if the face is not detected.'
					'Also, might work only if the face is not moving around much. Syntax: (top, bottom, left, right).')

parser.add_argument('--rotate', default=False, action='store_true',
					help='Sometimes videos taken from a phone can be flipped 90deg. If true, will flip video right by 90deg.'
					'Use if you get a flipped result, despite feeding a normal looking video')

parser.add_argument('--nosmooth', default=False, action='store_true',
					help='Prevent smoothing face detections over a short temporal window')

args = parser.parse_args()
args.img_size = 96

mel_step_size = 16
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} for inference.'.format(device))

# if os.path.isfile(args.face) and args.face.split('.')[1] in ['jpg', 'png', 'jpeg']:
# 	args.static = True

def get_smoothened_boxes(boxes, T):
	for i in range(len(boxes)):
		if i + T > len(boxes):
			window = boxes[len(boxes) - T:]
		else:
			window = boxes[i : i + T]
		boxes[i] = np.mean(window, axis=0)
	return boxes


# # 编写路由，构建url与函数的映射关系（将函数与url绑定）
# @app.route("/users",methods=["GET"])
# def users():
#     return jsonify({"code":10000,"message":"success","data":users_list})

# 视频文件预处理成numpy.ndarray，保存在内存中
@app.route("/synthesis/preVideoHandle",methods=["POST"])
def preVideoHandle():
    checkpointPath = request.json.get("checkpointPath")
    face = request.json.get("face")
    print("face = ",face)
    audioPath = request.json.get("audio")
    if not os.path.isfile(face):
        raise ValueError('--face argument must be a valid path to video/image file')
    elif face.split('.')[1] in ['jpg', 'png', 'jpeg']:
        full_frames = [cv2.imread(face)]
        fps = args.fps

    else:
        T1 = time.time()

        video_stream = cv2.VideoCapture(face)
        fps = video_stream.get(cv2.CAP_PROP_FPS)

        print('Reading video frames...')

        full_frames = []
        while 1:
            still_reading, frame = video_stream.read()
            if not still_reading:
                video_stream.release()
                break
            if args.resize_factor > 1:
                frame = cv2.resize(frame, (frame.shape[1]//args.resize_factor, frame.shape[0]//args.resize_factor))

            if args.rotate:
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

            y1, y2, x1, x2 = args.crop
            if x2 == -1: x2 = frame.shape[1]
            if y2 == -1: y2 = frame.shape[0]

            frame = frame[y1:y2, x1:x2]
            print("frame:",type(frame))
            full_frames.append(frame)
    cache.set(1,full_frames)
    cache.set('fps',fps)     
    print ("Number of frames available for inference: "+str(len(full_frames)))
    return   jsonify({"code":0000,"message":"缓存完成"})









@app.route("/synthesis/compose",methods=["POST"])
def compose():
    T1 = time.time()

    checkpointPath = request.json.get("checkpointPath")
    face = request.json.get("face")
    print("face = ",face)
    audioPath = request.json.get("audio")
    # if not os.path.isfile(face):
    #     raise ValueError('--face argument must be a valid path to video/image file')
    # elif face.split('.')[1] in ['jpg', 'png', 'jpeg']:
    #     full_frames = [cv2.imread(face)]
    #     fps = args.fps

    # else:
    #     T1 = time.time()

    #     video_stream = cv2.VideoCapture(face)
    #     fps = video_stream.get(cv2.CAP_PROP_FPS)

    #     print('Reading video frames...')

    #     full_frames = []
    #     while 1:
    #         still_reading, frame = video_stream.read()
    #         if not still_reading:
    #             video_stream.release()
    #             break
    #         if args.resize_factor > 1:
    #             frame = cv2.resize(frame, (frame.shape[1]//args.resize_factor, frame.shape[0]//args.resize_factor))

    #         if args.rotate:
    #             frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

    #         y1, y2, x1, x2 = args.crop
    #         if x2 == -1: x2 = frame.shape[1]
    #         if y2 == -1: y2 = frame.shape[0]

    #         frame = frame[y1:y2, x1:x2]
    #         print("frame:",type(frame))

    #         full_frames.append(frame)
    full_frames = cache.get(1)
    print('cache.get = ',full_frames[0])
    print ("Number of frames available for inference: "+str(len(full_frames)))
    T2 = time.time()
    print('读取视频帧-程序运行时间:%s毫秒' % ((T2 - T1)*1000))
    # 读取视频帧-程序运行时间:14938.355445861816毫秒

# 驱动语音的提取，处理至语音流的形式，小段流。TODO 将其提取出来单独做，输出为mel值
    if not audioPath.endswith('.wav'):
        print('Extracting raw audio...')
        command = 'ffmpeg -y -i {} -strict -2 {}'.format(audioPath, 'temp/temp.wav')

        subprocess.call(command, shell=True)
        audioPath = 'temp/temp.wav'
    T3 = time.time()

    wav = audio.load_wav(audioPath, 16000)
    mel = audio.melspectrogram(wav)
    print(mel.shape)
    T4 = time.time()
    print('读取驱动梅尔值-程序运行时间:%s毫秒' % ((T4 - T3)*1000))
# 读取驱动梅尔值-程序运行时间:42.38009452819824毫秒
    if np.isnan(mel.reshape(-1)).sum() > 0:
        raise ValueError('Mel contains nan! Using a TTS voice? Add a small epsilon noise to the wav file and try again')

    mel_chunks = []
    fps = cache.get('fps')
    mel_idx_multiplier = 80./fps 
    i = 0
    while 1:
        start_idx = int(i * mel_idx_multiplier)
        if start_idx + mel_step_size > len(mel[0]):
            mel_chunks.append(mel[:, len(mel[0]) - mel_step_size:])
            break
        mel_chunks.append(mel[:, start_idx : start_idx + mel_step_size])
        i += 1

    print("Length of mel chunks: {}".format(len(mel_chunks)))

    full_frames = full_frames[:len(mel_chunks)]

    batch_size = args.wav2lip_batch_size
    gen = datagen(full_frames.copy(), mel_chunks)
    

    for i, (img_batch, mel_batch, frames, coords) in enumerate(tqdm(gen, 
											total=int(np.ceil(float(len(mel_chunks))/batch_size)))):
        if i == 0:
			# model = load_model(args.checkpoint_path)
			# print ("Model loaded")
			# ort_session = onnxruntime.InferenceSession("/data/pkg/virtual/wav2lip1.onnx")

            frame_h, frame_w = full_frames[0].shape[:-1]
            out = cv2.VideoWriter('temp/result.avi', 
									cv2.VideoWriter_fourcc(*'DIVX'), fps, (frame_w, frame_h))
        T6 = time.time()
        img_batch = torch.FloatTensor(np.transpose(img_batch, (0, 3, 1, 2))).to(device)
        mel_batch = torch.FloatTensor(np.transpose(mel_batch, (0, 3, 1, 2))).to(device)
        ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(mel_batch),ort_session.get_inputs()[1].name: to_numpy(img_batch)}

        with torch.no_grad():
            ort_outs = ort_session.run(None, ort_inputs)
            out_outs1 = torch.from_numpy(ort_outs[0])

			# pred = model(mel_batch, img_batch)

		# pred = pred.cpu().numpy().transpose(0, 2, 3, 1) * 255.
        pred = out_outs1.cpu().numpy().transpose(0, 2, 3, 1) * 255.
        T8 = time.time()

        for p, f, c in zip(pred, frames, coords):
            y1, y2, x1, x2 = c
            p = cv2.resize(p.astype(np.uint8), (x2 - x1, y2 - y1))

            f[y1:y2, x1:x2] = p
            out.write(f)
        T7 = time.time()
        print('模型合成-程序运行时间:%s毫秒' % ((T7 - T8)*1000))

        print('模型合成-程序运行时间:%s毫秒' % ((T7 - T6)*1000))

    out.release()
# 优化处理逻辑 TODO  
    T5 = time.time()

    command = 'ffmpeg -y -i {} -i {} -strict -2 -q:v 1 {}'.format(audioPath, 'temp/result.avi', args.outfile)
    subprocess.call(command, shell=platform.system() != 'Windows')

    T6 = time.time()
    print('合成视频-程序运行时间:%s毫秒' % ((T4 - T3)*1000))

    return   jsonify({"code":0000,"message":"生成ok"})

def loadOnnxModel(onnxPatn):
 	return onnxruntime.InferenceSession(onnxPatn,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'])
 

def to_numpy(tensor):
    
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

def datagen(frames, mels):
	img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

	if args.box[0] == -1:
		if not args.static:
			face_det_results = face_detect(frames) # BGR2RGB for CNN face detection
		else:
			face_det_results = face_detect([frames[0]])
	else:
		print('Using the specified bounding box instead of face detection...')
		y1, y2, x1, x2 = args.box
		face_det_results = [[f[y1: y2, x1:x2], (y1, y2, x1, x2)] for f in frames]

	for i, m in enumerate(mels):
		idx = 0 if args.static else i%len(frames)
		frame_to_save = frames[idx].copy()
		face, coords = face_det_results[idx].copy()
		# print("检查坐标情况:",face_det_results)
		face = cv2.resize(face, (args.img_size, args.img_size))
			
		img_batch.append(face)
		mel_batch.append(m)
		frame_batch.append(frame_to_save)
		coords_batch.append(coords)

		if len(img_batch) >= args.wav2lip_batch_size:
			img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

			img_masked = img_batch.copy()
			img_masked[:, args.img_size//2:] = 0

			img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
			mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

			yield img_batch, mel_batch, frame_batch, coords_batch
			img_batch, mel_batch, frame_batch, coords_batch = [], [], [], []

	if len(img_batch) > 0:
		img_batch, mel_batch = np.asarray(img_batch), np.asarray(mel_batch)

		img_masked = img_batch.copy()
		img_masked[:, args.img_size//2:] = 0

		img_batch = np.concatenate((img_masked, img_batch), axis=3) / 255.
		mel_batch = np.reshape(mel_batch, [len(mel_batch), mel_batch.shape[1], mel_batch.shape[2], 1])

		yield img_batch, mel_batch, frame_batch, coords_batch
    
# 提取出来 提前做
def face_detect(images):
	detector = face_detection.FaceAlignment(face_detection.LandmarksType._2D, 
											flip_input=False, device=device)

	batch_size = args.face_det_batch_size
	
	while 1:
		predictions = []
		try:
			for i in tqdm(range(0, len(images), batch_size)):
				predictions.extend(detector.get_detections_for_batch(np.array(images[i:i + batch_size])))
		except RuntimeError:
			if batch_size == 1: 
				raise RuntimeError('Image too big to run face detection on GPU. Please use the --resize_factor argument')
			batch_size //= 2
			print('Recovering from OOM error; New batch size: {}'.format(batch_size))
			continue
		break

	results = []
	pady1, pady2, padx1, padx2 = args.pads
	for rect, image in zip(predictions, images):
		if rect is None:
			cv2.imwrite('temp/faulty_frame.jpg', image) # check this frame where the face was not detected.
			raise ValueError('Face not detected! Ensure the video contains a face in all the frames.')

		y1 = max(0, rect[1] - pady1)
		y2 = min(image.shape[0], rect[3] + pady2)
		x1 = max(0, rect[0] - padx1)
		x2 = min(image.shape[1], rect[2] + padx2)
		
		results.append([x1, y1, x2, y2])
		print(y1,y2,x1,x2)
	boxes = np.array(results)
	if not args.nosmooth: boxes = get_smoothened_boxes(boxes, T=5)
	results = [[image[y1: y2, x1:x2], (y1, y2, x1, x2)] for image, (x1, y1, x2, y2) in zip(images, boxes)]

	del detector
	return results 
   

if __name__ == '__main__':
    # 默认方式启动
    # app.run()
    # 解决jsonify中文乱码问题
    # 启动时加载模型

    global  ort_session 

    global full_frames


    ort_session  = loadOnnxModel("/data/pkg/virtual/wav2lip1.onnx")

    app.config['JSON_AS_ASCII'] = False
    print("启动服务")
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0",port=8899,debug=True,threaded=True)



 
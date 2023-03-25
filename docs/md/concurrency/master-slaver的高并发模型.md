

package com.crazymakercircle.designmodel.masterworker;
     // 省略import
     public class Worker<T extends Task, R>
     {
         //接收任务的阻塞队列
         private LinkedBlockingQueue<T> taskQueue = new LinkedBlockingQueue<>();
         //Worker 的编号
         static AtomicInteger index = new AtomicInteger(1);
         private int workerId;
         //执行任务的线程
         private Thread thread = null;
         public Worker()
         {
             this.workerId = index.getAndIncrement();
             thread = new Thread(() -> this.run());
             thread.start();
         }
     
         /**
          * 轮询执行任务
          */
         public void run()
         {
             // 轮询启动所有的子任务
             for (; ; )
             {
                 try
                 {
                     //从阻塞队列中提取任务
                     T task = this.taskQueue.take();
                     task.setWorkerId(workerId);
                     task.execute();
     
                 } catch (InterruptedException e)
                 {
                     e.printStackTrace();
                 }
             }
         }
     
         //接收任务到异步队列
         public void submit(T task, Consumer<R> action)
         {
             task.resultAction = action;  //设置任务的回调方法
             try{
                 this.taskQueue.put(task);
             } catch (InterruptedException e)
             {
                 e.printStackTrace();
             }
         }
     
     
     }


     package com.crazymakercircle.designmodel.masterworker;
     // 省略import
     @Data
     public class Task<R>
     {
         static AtomicInteger index = new AtomicInteger(1);
         //任务的回调函数
         public Consumer<Task<R>> resultAction;
         //任务的id
         private int id;
     
         // worker ID
         private int workerId;
     
         //计算结果
         R result = null;
     
         public Task()
         {
             this.id = index.getAndIncrement();
         }
     
         public void execute()
         {
             this.result = this.doExecute();
             //执行回调函数
             resultAction.accept(this);
         }
     
         //由子类实现
         protected R doExecute()
         {
             return null;
         }
     }


    
今天看的call：
轮询15s
50个线程处理会话维度信息，这个50个线程只是将会话任务提交出去了，并不会发生阻塞。只会持续不断地提交会话出去，处理时间不会拉很长。
真正同时完成高并发的部分在vcm。
明天看看你vcm的设计。

对于虚拟人中控来说，是实实在在的占用一个线程，到用户释放会话时释放资源。
--优化方向：
多线程优化：
master模式，提供连接的队列， redis队列。有序数组：userId
slaver：获取有序数组，多线程推送结果给app前端。  减少线程hold住的时间。


（主线程）master 内存有序队列 ConcurrentLinkedQueue  taskQueue 存储待处理的userId

worker： 启动一个线程循环监控Queue （或者说订阅）：以下操作为并发操作：
     查询redis该userId是否需要推送，如果需要则推送给前端。

考虑多机模型：
     1、放在内存中，减少重复userId的扫描



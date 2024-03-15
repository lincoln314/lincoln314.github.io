# es检索的几个关键点

[Similarity module | Elasticsearch Guide [8.12] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/8.12/index-modules-similarity.html)

1. 关键字使用 terms包含

   1. terms不再分词，使用分好的词进行查询
   2. keywords字段的type中设置后，其也不再分词
   3. term不会再计算分数，所有有这个关键字的就检索出来。所以如果还要加上评分的机制，在过滤的基础上再加上match来做分数计算
   4. term的效率比较快，直接通过倒排索引获取相关内容
2. should与must：

   1. should是 或关系
   2. must是且关系
3. match与term配合应用

   1. term进行关键字检索，match进一步打分，或者knn检索进一步打分
4. score的计算

   **仅做关键字业务，可以忽略tf的计算，直接使用idf进行打分**

   1. 在写index的时候，自定义分数计算脚本(similarity模块)，并在该字段计算上使用该脚本
   2. 默认BM25 文档的长度会对关键词打分计算有较大的影响，可通过调整k1跟b值，来调整文档长度对打分的影响
   3. 仅用term进行检索，term是不会计算分数的，所有有的全部检索出来。

   ```json
   PUT/index
   {
     "settings":{
       "number_of_shards":1,
       "similarity":{
         "scripted_tfidf":{
           "type":"scripted",
           "script":{
             "source":"double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
           }
         }
       }
     },
     "mappings":{
       "properties":{
         "field":{
           "type":"text",
           "similarity":"scripted_tfidf"
         }
       }
     }
   }
   ```
5. filter与term的选择：

   选择 `term` 还是 `filter` 取决于你的查询需求。如果你想要精确匹配某个字段的值，并且不关心评分，那么 `term` 查询通常更适合。如果你想要过滤出符合某个条件的文档，而不影响评分，那么 `filter` 上下文是一个更灵活的选择。

```json
GET /index_name/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "field_name": "exact_value"
          }
        },
        {
          "range": {
            "numeric_field": {
              "gte": 10
            }
          }
        }
      ]
    }
  }
}
```

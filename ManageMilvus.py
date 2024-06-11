import os
from langchain_huggingface import HuggingFaceEmbeddings
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections
from typing import Optional


class MilvusOperator:
    
    def __init__(self, 
                 collection_name: str, 
                 embedding_model: str = None
                 ) -> None:
        
        connections.connect(
            alias="default",
            host="127.0.0.1",
            port="19530"
        )
        self.collection_name = collection_name
        
        if embedding_model is  not None:
            self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)
        else:
            self.embedding = None
            
    def create_collection(self):  # 创建 collection_name的集合，参数有'id'、'text'、'vector'
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64,
                        is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024)
        ]
        schema = CollectionSchema(fields, self.collection_name)

        collection = self.get_Collection(schema=schema)

        default_index = {"index_type": "HNSW", "metric_type": "COSINE",
                         "params": {"M": 8, "efConstruction": 64}}
        
        _ = collection.create_index(field_name="vector", index_params=default_index)    
        

    def drop_collection(self):  # 删除 Milvus的collection_name 集合

        # 获取集合对象
        collection = self.get_Collection()

        # 删除集合
        collection.drop()
        
    def insert_collection(self, text):
        if self.embedding is None:
            raise ValueError("The embedding model was not loaded")
        
        collection = self.get_Collection()
        dosc_embedding = self.embedding.embed_documents([text])[0]

        entities = [
            {
                "vector": dosc_embedding,
                "text": text
            }
        ]

        ids = collection.insert(entities)
        collection.load()
        print(f"Data inserted into Milvus successfully. ID：{ids.primary_keys}")

    def get_Collection(self, schema: Optional[CollectionSchema] = None):
        if schema is None:
            collection = Collection(self.collection_name)
        else:
            collection = Collection(self.collection_name, schema=schema)
        return collection

    def query_search(self, query, limit=5):
        '''
        arguments:
            query:
                query represents the issue queried by the user.
            limit:
                Limit represents the retrieved data, with a default value of five

        return:
            result:
                The Limit articles with the highest similarity
        '''
        
        if self.embedding is None:
            raise ValueError("The embedding model was not loaded")
        
        collection = self.get_Collection()

        query_embedding = self.embedding.embed_documents([query])[0]

        search_params = {"metric_type": "COSINE", "params": {"M": 8, "efConstruction": 64}}

        results = collection.search(
            data=[query_embedding],  # 查询向量
            anns_field="vector",  # 存储嵌入的列名
            param=search_params,
            limit=limit,  # 返回的结果数量
            output_fields=["text"]  # 返回的字段
        )

        result = []

        for res in results[0]:
            result.append(res.entity.get('text'))
        return result



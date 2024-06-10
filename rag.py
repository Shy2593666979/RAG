import json

from model import chat_model
from operator import itemgetter
from FlagEmbedding import FlagReranker
from ManageMilvus import MilvusOperator

from . import EMBEDDING_MODEL, RERANKER_MODEL, COLLECTION_NAME


reranker = FlagReranker(RERANKER_MODEL,cache_dir=r"D:\LLM")

def rerank(query: str, passages: list, top_k: int):
    scores = reranker.compute_score([[query, page] for page in passages ])

    if isinstance(scores, list):
        similarity_dict = {page:scores[i] for i, page in enumerate(passages)}
    else:
        similarity_dict = {page:scores for i, page in enumerate(passages)}
    
    sorted_result = sorted(similarity_dict.items(), key=itemgetter(1), reverse=True)
    
    result = {}
    
    # 选取得分较高的top_k个数据
    for i in range(top_k):
        result[sorted_result[i][0]] = sorted_result[i][1]
        
    return result
    
    
    
if __name__ == "__main__":
    
    milvus = MilvusOperator(collection_name=COLLECTION_NAME, embedding_model=EMBEDDING_MODEL)
    query = "田明广做的任务是什么？"
    
    embedding_result = milvus.query_search(query)
    
    result = rerank(query, embedding_result, top_k=3)
    help_prompt = f"""
        #已知信息：
            {result}
        #用户问题：
            {query}
        请你结合已知信息和用户问题来回答用户
    """
    response = chat_model(help_prompt)
    
    print("LLM: " + response)

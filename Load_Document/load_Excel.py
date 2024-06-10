import os, sys
from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

sys.path.append("..")
from ManageMilvus import MilvusOperator

# 导入 pandas 用于处理 Excel 文件
import pandas as pd

def Load_Excel_Milvus(milvus: Optional[MilvusOperator], file_path):
    # 使用 pandas 加载 Excel 文件
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # 假设我们只需要读取第一列的文本内容
    pages = df.iloc[:, 0].tolist()
    
    # 使用文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    
    # 分割文档内容
    doc_text = text_splitter.split_documents(pages)
    for text in doc_text:
        # 插入到 Milvus 中
        milvus.insert_collection(text.page_content)   
        
if __name__ == "__main__":
    
    file_path = r"xxxx"
    embedding_path = "BAAI/bge-large-zh-v1.5"
    collection_name = "document"
    
    # 将PDF文件加载到Milvus向量库中
    milvus = MilvusOperator(collection_name=collection_name, embedding_model=embedding_path)
    Load_Excel_Milvus(milvus, file_path)
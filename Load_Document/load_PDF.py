import os, sys
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional

sys.path.append("..")
from ManageMilvus import MilvusOperator


def Load_PDF_Milvus(milvus: Optional[MilvusOperator], file_path):
    
    
    loader = PyPDFLoader(file_path)
    
    pages = loader.load_and_split()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    
    dosc_text = text_splitter.split_documents(pages)
    for text in dosc_text:
        
        milvus.insert_collection(text.page_content)
    


    
if __name__ == "__main__":
    
    file_path = r"D:\go\111.pdf"
    embedding_path = "BAAI/bge-large-zh-v1.5"
    collection_name = "document"
    # 删除collection_name的集合
    # drop_collection(collection_name)
    
    # 创建collection_name的集合
    # create_collection(collection_name)
    
    # 将PDF文件加载到Milvus向量库中
    milvus = MilvusOperator(collection_name=collection_name, embedding_model=embedding_path)
    Load_PDF_Milvus(milvus, file_path)
    

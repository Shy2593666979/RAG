import os, sys
from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docx import Document

sys.path.append("..")
from ManageMilvus import MilvusOperator


def Load_Word_Milvus(milvus: Optional[MilvusOperator], file_path):
    # 使用 python-docx 加载 Word 文档
    doc = Document(file_path)
    
    # 读取文档内容
    pages = [p.text for p in doc.paragraphs]
    
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
    Load_Word_Milvus(milvus, file_path)
    
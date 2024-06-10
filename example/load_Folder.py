import sys
sys.path.append("..")

from help import get_folder_file
from Load_Document.load_Excel import Load_Excel_Milvus
from Load_Document.load_PDF import Load_PDF_Milvus
from Load_Document.load_Word import Load_Word_Milvus
from ManageMilvus import MilvusOperator
from __init__ import COLLECTION_NAME, EMBEDDING_MODEL
from typing import Optional


def load_folder_file(milvus :Optional[MilvusOperator], folder_path):
    all_file = get_folder_file(folder_path)
    
    for item in all_file:
        if item.endwith(".pdf"):
            Load_PDF_Milvus(milvus, item)
        elif item.endwith(".docx"):
            Load_Word_Milvus(milvus, item)
        elif item.endwith(".xlsx"):
            Load_Excel_Milvus(milvus, item)
        else:
            pass

if __name__ == "__main__":
    folder_path = r"D:\document"
    
    milvus = MilvusOperator(collection_name=COLLECTION_NAME, embedding_model=EMBEDDING_MODEL)
    
    load_folder_file(milvus,folder_path)
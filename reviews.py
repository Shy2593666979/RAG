from ManageMilvus import MilvusOperator
import pandas as pd
from datasets import Dataset
from Load_Document.load_Word import Load_Word_Milvus
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)


df = pd.read_excel('./cs.xlsx')

query_list = df['query'].tolist()
answer_list = df['answer'].tolist()

manager_milvus = MilvusOperator()

Load_Word_Milvus(manager_milvus, './test.docx')

model = ChatOpenAI(base_url='', api_key='', model='')


#创建prompt模板
template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use two sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""
 
#由模板生成prompt
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model | StrOutputParser()

answers = []
contexts = []

for qr in query_list:
    answers.append(chain.invoke({'question': qr, 'context': manager_milvus.query_search(qr)}))
    contexts.append(manager_milvus.query_search(qr))

data = {
    'question': query_list,
    'answer': answers,
    'context': contexts,
    'ground_truths': answer_list
}

dataset = Dataset.from_dict(data)
 
result = evaluate(
    dataset = dataset, 
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)
 
df = result.to_pandas()
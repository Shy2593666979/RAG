# RAG 检索增强生成

欢迎来到 RAG 检索增强生成！这是一个使用 OpenAI API 和 Milvus 向量数据库的问答系统，结合了检索增强生成（RAG）技术。

[一文读懂RAG检索增强生成](https://blog.csdn.net/m0_63743577/article/details/135588292?spm=1001.2014.3001.5502)

## 项目特点

- 结合了 OpenAI 的语言模型和 Milvus 向量数据库。
- 实现了文本的语义检索和重排。
- 支持多种文档格式的加载和处理，包括 PDF、Word 和 Excel。

## 项目流程
![image](https://github.com/Shy2593666979/RAG/assets/105286202/b4e71d9d-b1db-457a-a49c-762941ff435c)



## 安装

在开始之前，请确保你已经安装了 Python 环境。接着，使用 pip 安装所需的依赖包：

```bash
pip install -r requirements.txt
```
## 使用说明
配置你的 OpenAI API 密钥和 Milvus 服务信息，在 __init__.py 文件中设置相应的变量。

使用 load_Excel.py、load_PDF.py 或 load_Word.py 脚本来加载你的文档到 Milvus 向量数据库。

使用 rag.py 脚本进行问答交互。
### 加载文档
```shell
Excel: python load_Excel.py

PDF: python load_PDF.py

Word: python load_Word.py

```
### 问答交互
运行以下命令与模型进行交互：
```python
python rag.py
```

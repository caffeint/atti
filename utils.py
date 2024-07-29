import streamlit as st
import yaml
from langchain_core.callbacks.base import BaseCallbackHandler
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader, PDFPlumberLoader
# from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma, FAISS
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.messages.chat import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import loading




class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

 
def print_messages():
    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
        for chat_message in st.session_state["messages"]:
            st.chat_message(chat_message.role).write(chat_message.content)



# 파일을 캐시 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장합니다.
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 단계 1: 문서 로드(Load Documents)
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()

    # 단계 2: 문서 분할(Split Documents)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    split_documents = text_splitter.split_documents(docs)

    # 단계 3: 임베딩(Embedding) 생성
    embeddings = OpenAIEmbeddings()

    # 단계 4: DB 생성(Create DB) 및 저장
    # 벡터스토어를 생성합니다.
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    # 단계 5: 검색기(Retriever) 생성
    # 문서에 포함되어 있는 정보를 검색하고 생성합니다.
    retriever = vectorstore.as_retriever()
    return retriever




"""
나중에 PDF 말고 DOCX PPT 등 다양한 문서 처리를 할때 사용


# def embed_file(file_name):
#     doc_list = []

#     if '.pdf' in file_name:
#         loader = PyPDFLoader(file_path=file_name)
#         documents = loader.load_and_split()
#     elif '.docx' in file_name:
#         loader = Docx2txtLoader(file_path=file_name)
#         documents = loader.load_and_split()
#     elif '.pptx' in file_name:
#         loader = UnstructuredPowerPointLoader(file_path=file_name)
#         documents = loader.load_and_split()

#     doc_list.extend(documents)
#     return doc_list


# def tiktoken_len(text):
#     tokenizer = tiktoken.get_encoding("cl100k_base")
#     tokens = tokenizer.encode(text)
#     return len(tokens)

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size = 900,
#         chunk_overlap = 100,
#         length_function = tiktoken_len
#     )
#     chunks = text_splitter.split_documents(text)
#     return (chunks)


"""
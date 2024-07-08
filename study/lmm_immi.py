from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from api import config

os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

# 웹페이지 로더 설정
data_loader = WebBaseLoader(
    "https://support.enlighten.kr/hc/ko/articles/6931557576473-RE100-%EC%9D%B4%ED%96%89-%EB%B0%A9%EB%B2%95-%EC%A4%91-%EC%A7%81%EC%A0%91-PPA-%EC%A0%9C3%EC%9E%90-PPA%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94")

#data_loader = PyPDFLoader("C:/Users/김지민/Desktop/data/비용평가세부운영규정.pdf")

cache_dir = LocalFileStore("./.cache/")

# 텍스트 분할 설정
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=500,
    chunk_overlap=50
)

# 문서 로드 및 분할
docs = data_loader.load_and_split(text_splitter=splitter)

# 임베딩 생성 및 캐시에 저장
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./.cache/")
#vectorstore.persist()

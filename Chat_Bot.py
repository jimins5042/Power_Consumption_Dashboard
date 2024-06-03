from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.chains.retrieval_qa.base import RetrievalQA

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

import config
import os

class Chat_bot():
    def caching_flies(self):
        os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

        # 웹페이지 로더 설정
        data_loader = WebBaseLoader("https://en.wikipedia.org/wiki/Moon")
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
        vectorstore.persist()

    def caching_embeds(self):
        os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

        embeddings = OpenAIEmbeddings()
        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, "./.cache/")
        vectorstore = Chroma(embedding_function=cached_embeddings, persist_directory="./.cache/")

        # 검색기 설정
        retriever = vectorstore.as_retriever()

        # 질의응답 체인 설정
        model = ChatOpenAI()


        map_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    질문에 답하기 위해 필요한 내용이 제시된 문장들 내에 포함되어 있는지 확인하세요. 만약 관련된 내용이 없다면 다음 문장들을 그대로 반환해주세요 : ''
                    -------
                    {context}
                    """,
                ),
                ("human", "{question}"),
            ]
        )

        map_chain = map_prompt | model

        def map_docs(inputs):
            documents, question = inputs["documents"], inputs["question"]
            return "\n\n".join(
                map_chain.invoke({"context": doc.page_content, "question": question}).content
                for doc in documents
            )

        map_results = {
                          "documents": retriever,
                          "question": RunnablePassthrough(),
                      } | RunnableLambda(map_docs)

        reduce_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    주어진 문장들을 이용해 최종 답변을 작성해주세요. 만약 주어진 문장들 내에 답변을 위한 내용이 포함되어있지 않다면, 답변을 꾸며내지 말고, 모른다고 답해주세요.
                    ------
                    {context}
                    """,
                ),
                ("human", "{question}"),
            ]
        )

        reduce_chain = {"context": map_results, "question": RunnablePassthrough()} | reduce_prompt | model

        answer = reduce_chain.invoke("달에 사람이 처음 도착한 날짜는 언제야?")
        print(answer)

import os
from dotenv import load_dotenv

load_dotenv()

# 1. 모델 설정
# model define example
# 1) llm 모델
#    from langchain.llms import OpenAI
#    llm = OpenAI(model_name="text-davinci-003")
# 2) Chat 모델
#    from langchain.chat_models import ChatOpenAI
#    chat = ChatOpenAI(openai_api_key=_config_info["OPENAI_API_KEY"], model_name="gpt-3.5-turbo", temperature=0.7)

# 2. 임베딩 선택
# 1) OpenAI 임베딩
#    from langchain.embeddings.openai import OpenAIEmbeddings
#    embedding = OpenAIEmbeddings()
# 2) HuggingFace 임베딩
#    from langchain.embeddings import HuggingFaceEmbeddings
#    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

import streamlit as st
from utils import print_messages, StreamHandler, embed_file
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain_core.runnables import ConfigurableFieldSpec
# from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="아띠 GPT", page_icon="🧊")
st.title("🧊 느린학습자용GPT")

# API KEY 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
#""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 채팅 대화기록을 저장하는 store 세션 상태 변수
if "store" not in st.session_state:
    st.session_state["store"] = dict()
# 이전 대화 기록 출력해주는 코드


with st.sidebar:
    session_id = st.text_input("Session ID",value="chat_1")
    file = st.file_uploader(
        "파일 업로드",
        type=["pdf","txt","hwp","docx"],
    )

    if file:
        retriever = embed_file(file)

    clear_btn = st.button("대화기록 초기화")
    if clear_btn:
        st.session_state["messages"] = []
        st.experimental_rerun()


print_messages()



# # 세션 ID를 기반으로 세션 기록을 가져오는 함수
# def get_session_history(session_ids: str, chat_hist_id: str) -> BaseChatMessageHistory:
#     if (session_ids, chat_hist_id) not in st.session_state["store"]:  # 세션 ID가 store에 없는 경우
#         # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
#         st.session_state["store"][(session_ids, chat_hist_id)] = ChatMessageHistory()
#     return st.session_state["store"][(session_ids, chat_hist_id)]  # 해당 세션 ID에 대한 세션 기록 반환

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    if session_ids not in st.session_state["store"]:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환


if user_input := st.chat_input("메세지를 입력해주세요."):
    # 사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

    

    # AI의 답변 
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        # LLM을 사용하여 AI의 답변을 생성
    
        # 1. 모델 생성
        # 1-1 openai
        llm = ChatOpenAI(streaming=True, model="gpt-4o-mini", callbacks=[stream_handler],)
        # 1-2 ollama model load
        # llm = ChatOllama(model="EEVE-Korean-test:latest")
        # 2. 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "너는 경계선 지능인을 도와주는 친한 친구이자 선생님 역할을 해줘. \
                    너의 목표는 나의 질문에 대해 경계선 지능인도 이해하기 쉽게 설명을 해주는 것이 목표야. \
                    답변은 꼼꼼하게 절차에 맞게 상세히 알려줘. \
                    질문에 대한 답변은 한글로 대답해줘.",
                ),
                # 대화 기록을 변수로 사용, history 가 MessageHistory 의 key 가 됨
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),  # 사용자의 질문을 입력
            ]
        )
        chain = prompt | llm

        chain_with_memory = (
            RunnableWithMessageHistory(  # RunnableWithMessageHistory 객체 생성
                chain,  # 실행할 Runnable 객체
                get_session_history,  # 세션 기록을 가져오는 함수
                input_messages_key="question",  # 사용자 질문의 키
                history_messages_key="history",  # 기록 메시지의 키
                # history_factory_config=[
                #     ConfigurableFieldSpec(
                #         id="session_ids",
                #         annotation=str,
                #         name="sessionId",
                #         description="세션의 고유 식별번호",
                #         is_shared=True,
                #     ),
                #     ConfigurableFieldSpec(
                #         id="chat_hist_id",
                #         annotation=str,
                #         name="chatHistId",
                #         description="채팅기록 식별번호",
                #         is_shared=True,
                #     )
                # ]
            )
        )
        response = chain_with_memory.invoke(
            {"question": user_input},
            # 세션 ID 설정
            config={"configurable": {"session_id": session_id}},
        )
        st.session_state["messages"].append(
            ChatMessage(role="assistant", content=response.content)
            )
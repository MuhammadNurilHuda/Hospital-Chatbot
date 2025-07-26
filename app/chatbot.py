# File: app/chatbot.py
import os
from dotenv import load_dotenv
from app.logging import logger

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

load_dotenv()

# —─────────────────────────────────────────────────
# 1) Konfigurasi environment
REDIS_URL   = os.getenv("REDIS_URL")
API_KEY     = os.getenv("DEEPSEEK_API_KEY")
# Jangan log API_KEY apapun bentuknya

# —─────────────────────────────────────────────────
# 2) Definisi system & human prompt untuk membatasi topik
system_template = SystemMessagePromptTemplate.from_template(
    "You are a hospital appointment assistant. "
    "You only answer questions about scheduling, modifying, "
    "or canceling doctor appointments at the hospital. "
    "If the user asks anything else, politely redirect them to use other services."
)
human_template = HumanMessagePromptTemplate.from_template("{question}")
chat_prompt    = ChatPromptTemplate.from_messages([system_template, human_template])

# —─────────────────────────────────────────────────
# 3) Inisialisasi embeddings, vector store, dan LLM
embedding = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=API_KEY
)
vectordb = Chroma(
    persist_directory="vector_store",
    embedding_function=embedding
)
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=API_KEY
)

# —─────────────────────────────────────────────────
# 4) Kata kunci booking sederhana
BOOKING_KEYWORDS = ["booking", "buat janji", "reservasi", "pesan dokter"]

def get_response(user_input: str, session_id: str) -> str:
    logger.info(f"[Session {session_id}] Menerima input: {user_input}")

    # a) Intent booking
    if any(kw in user_input.lower() for kw in BOOKING_KEYWORDS):
        logger.debug(f"[Session {session_id}] Intent booking terdeteksi.")
        return (
            "Tentu! Silakan berikan informasi berikut:\n"
            "- Nama Lengkap\n"
            "- Nomor HP\n"
            "- Spesialis Dokter yang Anda butuhkan\n"
            "- Jadwal yang diinginkan"
        )

    # b) Bangun memory per session
    chat_history = RedisChatMessageHistory(session_id=session_id, url=REDIS_URL)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=False
    )

    # c) RAG chain dengan prompt khusus
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": chat_prompt}
    )

    # d) Jalankan chain
    logger.info(f"[Session {session_id}] ▶️ Memulai RAG chain")
    result = rag_chain({"question": user_input})
    logger.info(f"[Session {session_id}] ◀️ Selesai RAG chain")

    answer = result.get("answer", "Maaf, saya belum punya informasi untuk itu.")
    logger.debug(f"[Session {session_id}] Respons RAG: {answer}")
    return answer

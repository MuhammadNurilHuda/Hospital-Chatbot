# scripts\build_vectorstore.py

from dotenv import load_dotenv
import os

#LangChain
from langchain.document_loaders import SQLDatabase, SQLDatabaseChain


load_dotenv()

# --------Koneksi db------------------------------------------------------------------
db_url = os.getenv("DATABASE_URL")
loader = SQLDatabase.from_uri(db_url)

# --------Ekstrak record--------------------------------------------------------------
chain = SQLDatabaseChain.from_llm(
    llm=None,  # kita hanya ingin loader-nya
    database=loader
)
docs = []

# a) Hospital FAQ
for row in loader.run("SELECT question, answer FROM hospital_faq"):
    docs.append({
        "page_content": row["question"] + "\n" + row["answer"],
        "metadata": {"source": "hospital_faq"}
    })

# b) Doctors Schedule
for row in loader.run(
    "SELECT doctor_name, specialty, available_days, start_time, end_time "
    "FROM doctors_schedule"
):
    content = (
        f"{row['doctor_name']} ({row['specialty']})\n"
        f"Hari: {row['available_days']}\n"
        f"Jam: {row['start_time']}–{row['end_time']}"
    )
    docs.append({
        "page_content": content,
        "metadata": {"source": "doctors_schedule"}
    })

# c) Hospital Locations
for row in loader.run(
    "SELECT name, address, phone FROM hospital_locations"
):
    docs.append({
        "page_content": f"{row['name']}\n{row['address']}\nTelp: {row['phone']}",
        "metadata": {"source": "hospital_locations"}
    })

# d) Appointment Process
for row in loader.run(
    "SELECT step_order, title, description FROM appointment_process ORDER BY step_order"
):
    docs.append({
        "page_content": f"Step {row['step_order']}: {row['title']}\n{row['description']}",
        "metadata": {"source": "appointment_process"}
    })

# e) Emergency Services
for row in loader.run(
    "SELECT service_name, description, contact FROM emergency_services"
):
    docs.append({
        "page_content": f"{row['service_name']}\n{row['description']}\nKontak: {row['contact']}",
        "metadata": {"source": "emergency_services"}
    })

# f) Appointments
for row in loader.run("SELECT name, doctor_specialist, appointment_date FROM appointments"):
    docs.append({
        "page_content": (
            f"Appointment: {row['name']} dengan {row['doctor_specialist']} pada {row['appointment_date']}"
        ),
        "metadata": {"source": "appointments"}
    })

# -------------Chroma index-------------------------------------------------------------------
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY")
)

vectordb = Chroma.from_documents(docs, embeddings, persist_directory="vector_store")
vectordb.persist()
print("✅ Vector store siap di folder vector_store")

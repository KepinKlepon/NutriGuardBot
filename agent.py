# agen.py (Salin kode dari jawaban sebelumnya ke sini)
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Tentukan State untuk Graph
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# Inisialisasi Model Gemini dan Sistem Prompt
def create_nutriguard_agent(api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key,
        model_kwargs={"system_instruction": 
            "Anda adalah Nutri-Guard Bot, asisten gizi dan kesehatan yang hangat dan empatik. "
            "Jawablah dengan fokus pada fakta nutrisi, pencegahan, dan tips hidup sehat. "
            "Jangan pernah memberikan diagnosis, resep obat, atau menyarankan pengobatan tanpa konsultasi dokter."
        }
    )

    def generate_response(state):
        prompt = state["messages"][-1]
        response = llm.invoke(prompt)
        
        # Tambahkan Disclaimer Wajib
        disclaimer = "\n\n⚠️ **Peringatan Penting (Disclaimer):** Informasi ini hanya untuk tujuan edukasi dan bukan pengganti saran dari dokter atau ahli gizi profesional. Selalu konsultasikan masalah kesehatan Anda dengan ahli."
        final_answer = response.content + disclaimer
        
        return {"messages": [("assistant", final_answer)]}
    
    # Bangun Graph sederhana
    workflow = StateGraph(AgentState)
    workflow.add_node("response_generator", generate_response)
    workflow.set_entry_point("response_generator")
    workflow.add_edge("response_generator", END)

    app = workflow.compile()
    return app

# Fungsi untuk memanggil agen
def run_agent(app, prompt):
    inputs = {"messages": [("user", prompt)]}
    result = app.invoke(inputs)
    # LangGraph menyimpan pesan sebagai tuple (role, content)
    return result["messages"][-1][1]
import os
from openai import OpenAI
from dotenv import load_dotenv

from vector_store import retrieve_semantic
from tools import get_latest_health_summary, analyze_trend

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =====================================================
# 🧠 1. HEALTH EXPLANATION (for Analyze button)
# =====================================================

def generate_health_explanation(data, risks):
    prompt = f"""
    You are a healthcare assistant.

    Patient Data:
    {data}

    Risks:
    {risks}

    Instructions:
    - Explain the condition in simple terms
    - Include:
        • Blood sugar (HbA1c)
        • Blood pressure
        • BMI
        • Temperature (fever detection)
        • SpO2 (oxygen levels)
        • Heart rate (cardiac condition)
    - Highlight key risks clearly
    - Suggest lifestyle improvements
    - Do NOT provide medical diagnosis
    - Use bullet points for readability
    - Add this disclaimer at the end:
      "This is not medical advice. Please consult a doctor."
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =====================================================
# 🤖 2. CHAT (RAG + PATIENT CONTEXT)
# =====================================================

def generate_chat_response(user_query, df):
    # 📊 Patient recent data
    patient_context = df.tail(3).to_dict(orient="records") if not df.empty else []

    # 📚 Semantic retrieval (FAISS)
    retrieved_knowledge = retrieve_semantic(user_query)

    prompt = f"""
    You are a healthcare assistant.

    Patient recent records:
    {patient_context}

    Medical knowledge:
    {retrieved_knowledge}

    User question:
    {user_query}

    Instructions:
    - Use BOTH patient data and medical knowledge
    - Consider:
        • HbA1c (diabetes)
        • Blood pressure (hypertension)
        • BMI (obesity)
        • Temperature (fever)
        • SpO2 (oxygen level)
        • Heart rate (cardiac condition)
    - Give clear, structured answers (bullet points)
    - Suggest lifestyle improvements
    - Do NOT give medical diagnosis
    - Always include:
      "This is not medical advice. Please consult a doctor."
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content, retrieved_knowledge


# =====================================================
# 🧠 3. AGENT (TOOL + AI DECISION MAKING)
# =====================================================

def agent_response(user_query, df):
    query = user_query.lower()

    # 🧠 Tool-based decisions
    if "summary" in query or "latest report" in query:
        return get_latest_health_summary()

    elif "trend" in query or "improving" in query:
        return analyze_trend()

    # 🚨 Critical health checks (smart agent behavior)
    elif "oxygen" in query or "spo2" in query:
        if not df.empty:
            latest = df.iloc[-1]
            if latest["spo2"] < 95:
                return "⚠️ Your oxygen level is low. Please seek medical attention."

    elif "heart rate" in query:
        if not df.empty:
            latest = df.iloc[-1]
            if latest["heart_rate"] > 100:
                return "⚠️ High heart rate detected (Tachycardia). Consider rest and consult a doctor."
            elif latest["heart_rate"] < 60:
                return "⚠️ Low heart rate detected (Bradycardia). Monitor closely."

    elif "fever" in query or "temperature" in query:
        if not df.empty:
            latest = df.iloc[-1]
            if latest["temperature"] > 37.5:
                return "⚠️ You may have a fever. Stay hydrated and monitor symptoms."

    # 🤖 Default → RAG + AI
    response, _ = generate_chat_response(user_query, df)
    return response
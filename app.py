import streamlit as st
import random
from rules import evaluate_health
from ai import generate_health_explanation, generate_chat_response
from db import init_db, insert_record, fetch_records
from report import generate_pdf
from alerts import generate_alerts

# Initialize DB
init_db()

st.set_page_config(page_title="Virtual Health Assistants for Patient Monitoring", layout="wide")
st.title("🩺 Virtual Health Assistant for Patient Monitoring")

# ==============================
# 🔹 MODE SELECTION
# ==============================

mode = st.radio("Select Mode", ["Manual", "Auto"])

# ==============================
# 🔹 AUTO DATA FUNCTION
# ==============================

def get_patient_data():
    return {
        "weight": 81,
        "height": 1.80,
        "hba1c": round(random.uniform(5.5, 7.5), 1),
        "systolic": random.randint(110, 150),
        "diastolic": random.randint(70, 95),
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "spo2": random.randint(89, 100),
        "heart_rate": random.randint(60, 120)
    }

# ==============================
# 🔹 INPUT SECTION
# ==============================

st.header("📥 Health Data")

if mode == "Manual":
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        weight = st.number_input("Weight (kg)", min_value=0.0)
        height = st.number_input("Height (m)", min_value=0.0)

    with col2:
        hba1c = st.number_input("HbA1c (%)", min_value=0.0)

    with col3:
        systolic = st.number_input("Systolic BP", min_value=0.0)
        diastolic = st.number_input("Diastolic BP", min_value=0.0)

    with col4:
        temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0)
        spo2 = st.number_input("SpO2 (%)", min_value=0.0, max_value=100.0)
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=0)

else:
    auto_data = get_patient_data()

    weight = auto_data["weight"]
    height = auto_data["height"]
    hba1c = auto_data["hba1c"]
    systolic = auto_data["systolic"]
    diastolic = auto_data["diastolic"]
    temperature = auto_data["temperature"]
    spo2 = auto_data["spo2"]
    heart_rate = auto_data["heart_rate"]

    st.success("🤖 Auto Mode Enabled (Simulated Live Data)")
    st.json(auto_data)

    if st.button("🔄 Refresh Data"):
        st.rerun()

# BMI calculation
bmi = weight / (height ** 2) if height > 0 else None

# ==============================
# 🔹 ANALYSIS
# ==============================

analyze_clicked = st.button("Analyze")

if mode == "Auto":
    analyze_clicked = True

if analyze_clicked:
    data = {
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "hba1c": hba1c,
        "systolic": systolic,
        "diastolic": diastolic,
        "temperature": temperature,
        "spo2": spo2,
        "heart_rate": heart_rate
    }

    result = evaluate_health(data)
    insert_record(data, result["score"])
    explanation = generate_health_explanation(data, result["risks"])

    st.session_state["data"] = data
    st.session_state["result"] = result
    st.session_state["explanation"] = explanation

# ==============================
# 🔹 RESULTS + ALERTS
# ==============================

if "result" in st.session_state:

    data = st.session_state["data"]
    result = st.session_state["result"]
    explanation = st.session_state["explanation"]

    # 🔴 ALERT SYSTEM
    alerts = generate_alerts(data)

    if alerts:
        st.header("🚨 Health Alerts")

        if len(alerts) >= 2:
            st.error("🚨 Multiple risk factors detected. Immediate attention required.")

        for level, message in alerts:
            if level == "CRITICAL":
                st.error(message)
                st.toast(message)
            elif level == "WARNING":
                st.warning(message)
    else:
        st.success("✅ No critical alerts")

    # 📊 RESULTS DISPLAY
    st.header("📊 Analysis Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Health Score")
        st.success(f"{result['score']} / 100")

    with col2:
        st.subheader("Risks")
        if result["risks"]:
            st.warning(", ".join(result["risks"]))
        else:
            st.success("No major risks detected")

    st.subheader("🤖 AI Insights")
    st.markdown(explanation)

    # 📄 PDF GENERATION
    if st.button("📄 Generate Health Report"):
        file_path = generate_pdf(data, result, explanation)

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Report",
                data=f,
                file_name="health_report.pdf",
                mime="application/pdf"
            )

# ==============================
# 🔹 DATA SECTION
# ==============================

df = fetch_records()

st.header("📈 Health Trends")

if not df.empty:
    st.line_chart(df[["hba1c", "bmi", "systolic", "spo2", "heart_rate"]])
else:
    st.info("No data available yet")

st.header("📋 Patient History")
st.dataframe(df)

# ==============================
# 🔹 TREND INSIGHT
# ==============================

if len(df) >= 2:
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    st.header("🔍 Trend Insight")

    if latest["hba1c"] > previous["hba1c"]:
        st.warning("HbA1c is increasing ⚠️")
    else:
        st.success("HbA1c is improving ✅")

# ==============================
# 🔹 CHATBOT
# ==============================

st.header("💬 Ask Health Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something about your health...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    response, retrieved_knowledge = generate_chat_response(user_input, df)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

        if retrieved_knowledge:
            st.markdown("### 📚 Knowledge Used")
            st.info(retrieved_knowledge)
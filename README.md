🩺 Virtual Health Assistant for Patient Monitoring

An AI-powered healthcare application that analyzes patient vitals and lab parameters to provide real-time risk assessment, health scoring, and intelligent explanations using a combination of rule-based logic and Retrieval-Augmented Generation (RAG).

⸻

🚀 Overview

The Virtual Health Assistant helps monitor patient health using key medical inputs and provides:
• Risk detection (Diabetes, Hypertension, etc.)
• Health score calculation
• AI-generated explanations
• Preventive health insights

This system is designed to work effectively even with limited data, leveraging WHO-based medical thresholds and AI-powered reasoning.

⸻

🎯 Features

✅ Rule-based health evaluation system  
✅ Real-time health risk scoring (0–100)  
✅ Detection of critical conditions:  
• Diabetes / Prediabetes  
• Hypertension  
• Obesity / Overweight  
• Fever  
• Low Oxygen Levels  
• Abnormal Heart Rate  

✅ AI-powered explanation using RAG  
✅ Streamlit-based interactive UI  
✅ Lightweight and fast execution  

⸻

🧠 How It Works

1. User Input

The user provides:
• HbA1c  
• Blood Pressure (Systolic / Diastolic)  
• BMI  
• Temperature  
• SpO2  
• Heart Rate  

⸻

2. Rule-Based Engine

Health conditions are evaluated using predefined clinical rules:
• HbA1c → Diabetes classification  
• Blood Pressure → Hypertension detection  
• BMI → Obesity classification  
• SpO2 → Oxygen level check  
• Heart Rate → Tachycardia / Bradycardia  
• Temperature → Fever detection  

⸻

3. Health Score Calculation

• Initial Score: 100  
• Deductions applied based on detected risks  
• Final score normalized between 0–100  

⸻

4. RAG-Based AI Explanation

The system enhances interpretability using:
• knowledge.txt as medical knowledge base  
• Vector search (vector_store.py)  
• LLM-based explanation generation (ai.py)  

This produces human-readable health insights and recommendations.

⸻

🏗️ Architecture

User Input (Streamlit UI)
        ↓
Rule Engine (rules.py)
        ↓
Risk Detection + Score Calculation
        ↓
Context Builder
        ↓
Vector Search (RAG)
        ↓
LLM Explanation Generator
        ↓
Final Health Report

🛠️ Tech Stack

• Frontend: Streamlit  
• Backend Logic: Python  
• AI Layer: LLM (via ai.py)  
• RAG: Vector Store + Knowledge Base  
• Database: SQLite (health.db)  

⸻

📂 Project Structure

├── app.py                # Streamlit UI  
├── rules.py              # Rule-based health evaluation  
├── ai.py                 # LLM explanation generator  
├── vector_store.py       # RAG implementation  
├── knowledge.txt         # Medical knowledge base  
├── report.py             # Report generation  
├── alerts.py             # Alert system  
├── db.py                 # Database handling  
├── utils.py              # Utility functions  
├── tools.py              # Helper tools  
├── requirements.txt  
├── health.db  

⚙️ Installation

git clone https://github.com/your-username/virtual-health-assistant.git  
cd virtual-health-assistant  

pip install -r requirements.txt  

add your OpenAI API key to .env file:  
OPENAI_API_KEY=your_api_key_here  

▶️ Run the App

streamlit run app.py  

📊 Example Output

• Health Score: 72  
• Risk Level: Moderate  
• Detected Risks:  
• Prediabetes  
• Hypertension  

• AI Explanation:  
The patient’s HbA1c indicates elevated blood sugar levels. Combined with increased blood pressure, this suggests a higher risk of metabolic and cardiovascular complications.

⸻

🔮 Future Enhancements

• Integration with wearable devices (real-time vitals tracking)  
• Advanced ML-based prediction models for proactive risk detection  
• Multi-user patient monitoring dashboard for clinics and healthcare providers  
• Cloud deployment (AWS / GCP) for scalability and reliability  
• Mobile application for continuous health tracking  
• ECG Integration: Real-time cardiac signal analysis for arrhythmia and heart condition detection  
• EEG Integration: Brain signal processing for neurological monitoring, stress analysis, and early disorder detection  

⸻

⭐ Vision

To build an accessible, AI-driven preventive healthcare assistant that enables early detection, continuous monitoring, and smarter health decisions.

⚠️ Disclaimer

This application is intended for educational and monitoring purposes only.  
It is not a substitute for professional medical advice, diagnosis, or treatment.  
For any health concerns, please consult a qualified healthcare provider.
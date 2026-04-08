from db import fetch_records


def get_latest_health_summary():
    df = fetch_records()

    if df.empty:
        return "No data available"

    latest = df.iloc[-1]

    return f"""
### 📊 Latest Health Summary

- HbA1c: {latest['hba1c']}
- BMI: {latest['bmi']}
- Blood Pressure: {latest['systolic']}/{latest['diastolic']}
- Temperature: {latest['temperature']} °C
- SpO2: {latest['spo2']} %
- Heart Rate: {latest['heart_rate']} bpm
- Health Score: {latest['score']}
"""


def analyze_trend():
    df = fetch_records()

    if len(df) < 2:
        return "Not enough data to analyze trends"

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    insights = []

    if latest["hba1c"] > previous["hba1c"]:
        insights.append("⚠️ HbA1c is increasing")
    else:
        insights.append("✅ HbA1c is improving")

    if latest["spo2"] < previous["spo2"]:
        insights.append("⚠️ Oxygen level decreasing")

    if latest["heart_rate"] > previous["heart_rate"]:
        insights.append("⚠️ Heart rate increasing")

    return "\n".join(insights)
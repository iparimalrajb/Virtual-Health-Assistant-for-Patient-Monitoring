def generate_alerts(data):
    alerts = []

    # 🔴 SpO2 (Critical)
    if data.get("spo2") is not None:
        if data["spo2"] < 92:
            alerts.append(("CRITICAL", "🚨 Oxygen level is dangerously low (SpO2 < 92%)"))

    # 🔴 Heart Rate
    if data.get("heart_rate") is not None:
        if data["heart_rate"] > 110:
            alerts.append(("WARNING", "⚠️ High heart rate detected"))
        elif data["heart_rate"] < 55:
            alerts.append(("WARNING", "⚠️ Low heart rate detected"))

    # 🔴 Temperature
    if data.get("temperature") is not None:
        if data["temperature"] > 38:
            alerts.append(("WARNING", "🌡 High fever detected"))

    # 🔴 Blood Pressure
    if data.get("systolic") is not None:
        if data["systolic"] > 160:
            alerts.append(("CRITICAL", "🚨 High blood pressure (Hypertensive crisis)"))

    return alerts
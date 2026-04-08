def evaluate_health(data):
    results = {}
    score = 100
    risks = []

    # HbA1c
    hba1c = data.get("hba1c")
    if hba1c:
        if hba1c > 6.5:
            risks.append("Diabetes")
            score -= 25
        elif hba1c > 5.7:
            risks.append("Prediabetes")
            score -= 15

    # Blood Pressure
    sys = data.get("systolic")
    dia = data.get("diastolic")

    if sys and dia:
        if sys > 140 or dia > 90:
            risks.append("Hypertension")
            score -= 20

    # BMI
    bmi = data.get("bmi")
    if bmi:
        if bmi > 30:
            risks.append("Obese")
            score -= 20
        elif bmi > 25:
            risks.append("Overweight")
            score -= 10

    # Temperature
    temp = data.get("temperature")
    if temp:
        if temp > 37.5:
            risks.append("Fever")
            score -= 10

    # SpO2
    spo2 = data.get("spo2")
    if spo2:
        if spo2 < 95:
            risks.append("Low Oxygen Level")
            score -= 20

    # Heart Rate
    hr = data.get("heart_rate")
    if hr:
        if hr > 100:
            risks.append("High Heart Rate (Tachycardia)")
            score -= 15
    elif hr < 60:
        risks.append("Low Heart Rate (Bradycardia)")
        score -= 15

    results["score"] = max(score, 0)
    results["risks"] = risks

    return results
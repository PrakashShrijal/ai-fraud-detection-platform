from ml_engine.predict import predict_anomaly

def calculate_fraud(transaction):

    risk_score = 0
    reasons = []

    # Rule 1 — High Amount
    if transaction["amount"] > 7000:
        risk_score += 40
        reasons.append("High transaction amount")

    # Rule 2 — Midnight Transaction
    if transaction["hour"] >= 0 and transaction["hour"] <= 4:
        risk_score += 20
        reasons.append("Late night transaction")

    # Rule 3 — New Receiver
    if transaction["is_new_receiver"] == True:
        risk_score += 20
        reasons.append("New receiver detected")

    # Rule 4 — High Frequency
    if transaction["tx_count_last_1hr"] > 5:
        risk_score += 20
        reasons.append("Too many transactions in 1 hour")

    # Risk Level
    if risk_score >= 60:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # ML Prediction
    ml_result = predict_anomaly(transaction)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "fraud_reasons": reasons,
        "ml_prediction": ml_result
    }
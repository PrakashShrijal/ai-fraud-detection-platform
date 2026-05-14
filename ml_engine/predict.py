import pandas as pd
from sklearn.ensemble import IsolationForest

# Train temporary model
model = IsolationForest(
    contamination=0.3,
    random_state=42
)

# Dummy training data
training_data = pd.DataFrame([
    [1000, 12, 0, 1],
    [2000, 14, 0, 2],
    [500, 10, 0, 1],
    [8000, 2, 1, 7],
    [9500, 1, 1, 8],
    [7000, 3, 1, 6]
], columns=[
    "amount",
    "hour",
    "is_new_receiver",
    "tx_count_last_1hr"
])

model.fit(training_data)

def predict_anomaly(transaction):

    input_data = pd.DataFrame([[
        transaction["amount"],
        transaction["hour"],
        int(transaction["is_new_receiver"]),
        transaction["tx_count_last_1hr"]
    ]], columns=[
        "amount",
        "hour",
        "is_new_receiver",
        "tx_count_last_1hr"
    ])

    prediction = model.predict(input_data)[0]

    if prediction == -1:
        return "ANOMALY"

    return "NORMAL"
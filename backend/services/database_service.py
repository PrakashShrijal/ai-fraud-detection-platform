from backend.database.db import SessionLocal

from backend.models.transaction_db_model import TransactionDB

def save_transaction(transaction, fraud_result):

    db = SessionLocal()

    db_transaction = TransactionDB(

        amount=transaction["amount"],

        hour=transaction["hour"],

        is_new_receiver=transaction["is_new_receiver"],

        tx_count_last_1hr=transaction["tx_count_last_1hr"],

        risk_score=fraud_result["risk_score"],

        risk_level=fraud_result["risk_level"],

        ml_prediction=fraud_result["ml_prediction"]
    )

    db.add(db_transaction)

    db.commit()

    db.refresh(db_transaction)

    db.close()

    return db_transaction

def get_all_transactions():

    db = SessionLocal()

    transactions = db.query(TransactionDB).all()

    db.close()

    return transactions

def get_analytics():

    db = SessionLocal()

    transactions = db.query(TransactionDB).all()

    total_transactions = len(transactions)

    high_risk_count = len([
        tx for tx in transactions
        if tx.risk_level == "HIGH"
    ])

    anomaly_count = len([
        tx for tx in transactions
        if tx.ml_prediction == "ANOMALY"
    ])

    if total_transactions > 0:
        fraud_percentage = round(
            (anomaly_count / total_transactions) * 100,
            2
        )
    else:
        fraud_percentage = 0

    db.close()

    return {
        "total_transactions": total_transactions,
        "high_risk_transactions": high_risk_count,
        "anomaly_transactions": anomaly_count,
        "fraud_percentage": fraud_percentage
    }
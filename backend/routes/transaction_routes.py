from fastapi import APIRouter

from backend.models.transaction_model import Transaction

from backend.services.fraud_service import calculate_fraud

from backend.services.database_service import (
    save_transaction,
    get_all_transactions,
    get_analytics
)

from backend.realtime.websocket_manager import manager

from fastapi import Depends

from backend.auth.auth_bearer import JWTBearer

router = APIRouter()

@router.post("/predict")
async def predict_fraud(transaction: Transaction):

    transaction_data = transaction.dict()

    fraud_result = calculate_fraud(transaction_data)

    save_transaction(transaction_data, fraud_result)

        # Live Fraud Alert
    if fraud_result["risk_level"] == "HIGH":

        await manager.broadcast({
            "alert": "HIGH RISK TRANSACTION DETECTED",
            "transaction": transaction_data,
            "fraud_analysis": fraud_result
        })

    return {
        "transaction": transaction_data,
        "fraud_analysis": fraud_result
    }

@router.get(
    "/transactions",
    dependencies=[Depends(JWTBearer())]
)
def get_transactions():

    transactions = get_all_transactions()

    return transactions

@router.get(
    "/analytics",
    dependencies=[Depends(JWTBearer())]
)
def analytics():

    result = get_analytics()

    return result
from sqlalchemy import Column, Integer, Float, Boolean, String

from backend.database.db import Base

class TransactionDB(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float)
    hour = Column(Integer)

    is_new_receiver = Column(Boolean)

    tx_count_last_1hr = Column(Integer)

    risk_score = Column(Integer)

    risk_level = Column(String)

    ml_prediction = Column(String)
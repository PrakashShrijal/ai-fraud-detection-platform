from pydantic import BaseModel

class Transaction(BaseModel):

    amount: float
    hour: int
    is_new_receiver: bool
    tx_count_last_1hr: int
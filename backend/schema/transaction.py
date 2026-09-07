from pydantic import BaseModel

class UserTransactionRequest(BaseModel):
    receiver_id: int
    amount: int
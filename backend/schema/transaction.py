from pydantic import BaseModel

class UserTransactionRequest(BaseModel):
    sender_id: str
    receiver_id: str
    amount: int
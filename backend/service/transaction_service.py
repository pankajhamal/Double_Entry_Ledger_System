import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TransactionService:

    async def payment_service(self, payload) -> Dict[str, Any]:
        "User Transaction"
        data = payload.model_dump(mode="json")
        sender_id = str(data.get("sender_id"))
        receiver_id = str(data.get("receiver_id"))
        amount = int(data.get("amount"))

        logger.info(f"Entry Point Transfer Initiated. {amount} NPR from {sender_id} to {receiver_id}")

        try:
            await 
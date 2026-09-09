import logging
import uuid
import json
from fastapi import HTTPException, status
from typing import Dict, Any
from backend.models.account import Account
from backend.models.transaction import Transaction
from backend.models.ledger import Ledger
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.core.db_adapter import get_user_balance
from backend.core.exception import InsufficientBalanceError
from backend.core.redis import redis_client
logger = logging.getLogger("fast_api")

class TransactionService:

    async def payment_service(self, payload, current_user, idempotency_key, db:Session) -> Dict[str, Any]:
        "User Transaction"
        logger.info("Payment Service called.")
        print("PAYMENT SERVICE")

        sender_id = current_user.id
        receiver_id = payload.receiver_id
        amount = int(payload.amount)

        try:
            #Store idempotency key in redis
            cached_response = redis_client.get(
                f"idempotency:{idempotency_key}"
            )
            if cached_response:
                logger.info("IDEMPOTENCY CACHE HIT | key=%s", idempotency_key)
                return json.loads(cached_response)

            logger.info("IDEMPOTENCY CACHE MISS | key=%s", idempotency_key)
            
            #check idempotency
            existing_transaction = db.query(Transaction).filter(Transaction.idempotency_key == idempotency_key).first()
            if existing_transaction:
                return{
                    "message": "Transaction already proceed",
                    "transaction_id": existing_transaction.id,
                    "reference": existing_transaction.reference
                }

            if amount<=0:
                raise ValueError("Amount must be greater than 0")

            #Find sender account with select for update
            sender_account = db.query(Account).filter(Account.user_id == current_user.id).with_for_update().first()

            #Find receiver account
            receiver_account= db.query(Account).filter(Account.user_id == receiver_id).first()

            if sender_account is None:
                logger.info("Sender account not found")
                raise ValueError("Sender account not found")
            
            if receiver_account is None:
                logger.info("Receiver account not found.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Receiver account not found"
                )
            if sender_account.id == receiver_account.id:
                raise ValueError("Cannot transfer to yourself")

            #Check balance
            sender_balance = get_user_balance(
                sender_account.id,
                db
            )
            print(sender_balance)
            logger.info("SENDER BALANCE: %s", sender_balance)

            if sender_balance<amount:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Insufficient Balance"
                )

            transaction = Transaction(
                reference = f"FUND TRANSFER-{uuid.uuid4().hex[:12].upper()}",
                description = f"Transafer fund",
                idempotency_key=idempotency_key
            )
            db.add(transaction)
            db.flush()

            sender_entry = Ledger(
                transaction_id = transaction.id,
                account_id = sender_account.id,
                debit = 0,
                credit = amount,
            )

            receiver_entry = Ledger(
                transaction_id = transaction.id,
                account_id = receiver_account.id,
                debit = amount,
                credit = 0
            )
            db.add(sender_entry)
            db.add(receiver_entry)

            db.commit()

            response = {
                "message": "Payment successfull",
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "amount": amount
            }

            redis_client.set(
                f"idempotency:{idempotency_key}",
                json.dumps(response),
                ex=86400
            )

            return response

        except IntegrityError:
            db.rollback()

            existing_transaction = db.query(Transaction).filter(Transaction.idempotency_key == idempotency_key).first()
            if existing_transaction:
                return {
                    "message": "Transaction already proceed",
                    "transaction_id": existing_transaction.id,
                    "reference": existing_transaction.reference
                }
            raise

        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            logger.exception("Payment failed | sender=%s receiver=%s", sender_id, receiver_id)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Paymen processing failed"
            )
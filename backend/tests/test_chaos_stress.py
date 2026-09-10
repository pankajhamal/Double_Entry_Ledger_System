import asyncio
import pytest
import httpx

URL = "http://127.0.0.1:8000/user/payment"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg5MDE4MDM0fQ.deeoxHpHUypldl04PHVPKlF5HygtmR6A_ZEtT7wTD_o"
RECEIVER_ID = 2


@pytest.mark.asyncio
async def test_concurrent_payment():

    async with httpx.AsyncClient() as client:

        async def payment(number):
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Idempotency-Key": f"withdraw-1000-{number}",
            }

            payload = {
                "receiver_id": RECEIVER_ID,
                "amount": 100,
            }

            response = await client.post(
                URL,
                json=payload,
                headers=headers,
            )

            print(
                f"Request {number}: "
                f"{response.status_code} - {response.text}"
            )

            return response.status_code

        tasks = [
            payment(i)
            for i in range(1, 501)
        ]

        results = await asyncio.gather(*tasks)

    print("Results:", results)

    success = results.count(200)
    insufficient = results.count(402)

    print("Successful:", success)
    print("Insufficient:", insufficient)

    assert success == 10
    assert insufficient == 0
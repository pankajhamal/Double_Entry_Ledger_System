import redis
from fastapi import HTTPException, status

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def check_rate_limit(user_id: int):
    key = f"rate_limit:user:{user_id}"

    current_count = redis_client.incr(key)

    if current_count == 1:
        redis_client.expire(key, 60)

    if current_count > 60:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="To Many Request"
        )
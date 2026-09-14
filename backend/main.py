from fastapi import FastAPI
import uvicorn
from backend.core.database import Base, engine
import backend.models
from backend.routers.users import router as auth_router
from backend.routers.transaction import router as payment_router
from backend.core.logger import logger

from contextlib import asynccontextmanager
from backend.infrastructure.rabbitmq import rabbitmq

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
  #Startup
  logger.info("Connecting to RabbitMQ...")
  await rabbitmq.connect()
  logger.info("RabbitMQ connected successfully")

  yield

  #shutdown
  logger.info("Closing RabbitMQ connection...")
  await rabbitmq.close()
  logger.info("RabbitMQ connection closed")

app = FastAPI(
  title="Double Entry Leader System",
  version="1.0.0",
  lifespan=lifespan
)

@app.get("/")
def read_root():
  logger.info("Root endpoint accessed")
  return {"Helllo" : "World"}

app.include_router(auth_router)
app.include_router(payment_router)


if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
  )
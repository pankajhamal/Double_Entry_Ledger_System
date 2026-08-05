from fastapi import FastAPI
import uvicorn
from backend.core.database import Base, engine
import backend.models
from backend.routers.users import router as auth_router
from backend.core.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
  title="Double Entry Leader System",
  version="1.0.0"
)

@app.get("/")
def read_root():
  logger.info("Root endpoint accessed")
  return {"Helllo" : "World"}

app.include_router(auth_router)

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
  )
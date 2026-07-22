from fastapi import FastAPI
import uvicorn
from core.database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
  title="Double Entry Leader System",
  version="1.0.0"
)

@app.get("/")
def read_root():
  return {"Helllo" : "World"}

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
  )
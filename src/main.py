import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routes.process_routes import router as process_router

load_dotenv()

app = FastAPI(
    title="Process Handler API",
    description="API for extracting and analyzing legal process PDFs",
    version="1.0.0"
)

app.include_router(process_router, tags=["Process"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Any
import asyncio

from application.dto import ExtractProcessRequest
from domain.schemas import ProcessExtraction
from application.services import ProcessExtractionService
from infrastructure.llm_client import GeminiLlmClient
from infrastructure.storage import SqliteRepository
from infrastructure.pdf_downloader import PdfDownloader

router = APIRouter()
storage = SqliteRepository()

@router.on_event("startup")
async def startup_event() -> None:
    await storage.initialize()

@router.post("/extract", response_model=ProcessExtraction)
async def extract_process(request: ExtractProcessRequest) -> Any:
    try:
        service = ProcessExtractionService(
            llm_client=GeminiLlmClient(),
            storage=storage,
            pdf_downloader=PdfDownloader()
        )
        
        try:
            result = await asyncio.wait_for(
                service.extract_process(request),
                timeout=300
            )
            return result
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504, 
                detail="The request timed out. The process might be too large or complex. Please try with a smaller PDF or contact support."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

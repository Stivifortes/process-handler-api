import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from domain.schemas import ProcessExtraction, TimelineEvent, Evidence
from infrastructure.llm_client import GeminiLlmClient
from infrastructure.storage import SqliteRepository, Base
from infrastructure.pdf_downloader import PdfDownloader

TEST_DB_PATH = "test_process_handler.db"
TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

@pytest.fixture
async def test_db():
    engine = create_async_engine(TEST_DB_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    try:
        yield engine
    finally:
        await engine.dispose()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

@pytest.fixture
def mock_llm_client():
    client = AsyncMock(spec=GeminiLlmClient)
    client.analyze_pdf.return_value = ProcessExtraction(
        case_id="test-case",
        resume="Test summary",
        timeline=[
            TimelineEvent(
                event_id=1,
                event_name="Test Event",
                event_description="Test Description",
                event_date="2025-01-01",
                event_page_init=1,
                event_page_end=2
            )
        ],
        evidence=[
            Evidence(
                evidence_id=1,
                evidence_name="Test Evidence",
                evidence_flaw=None,
                evidence_page_init=3,
                evidence_page_end=4
            )
        ],
        persisted_at=datetime.utcnow()
    )
    return client

@pytest.fixture
async def test_storage(test_db):
    repository = SqliteRepository()
    repository.engine = test_db
    repository.async_session = sessionmaker(
        test_db, class_=AsyncSession, expire_on_commit=False
    )
    await repository.initialize()
    return repository

@pytest.fixture
def mock_pdf_downloader():
    downloader = AsyncMock(spec=PdfDownloader)
    downloader.download_pdf.return_value = MagicMock()
    return downloader

@pytest.fixture
def client(test_storage):
    app.state.storage = test_storage
    return TestClient(app)

@pytest.mark.asyncio
async def test_extract_process_endpoint(client, test_storage):
    test_request = {
        "pdf_url": "https://example.com/test.pdf",
        "case_id": "test-case-123"
    }
    
    response = client.post("/extract", json=test_request)
    
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == test_request["case_id"]
    assert "resume" in data
    assert "timeline" in data
    assert "evidence" in data
    assert "persisted_at" in data
    
    async with test_storage.async_session() as session:
        result = await session.get(ProcessExtractionModel, test_request["case_id"])
        assert result is not None
        assert result.case_id == test_request["case_id"]

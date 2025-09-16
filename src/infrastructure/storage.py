import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy import JSON, String, DateTime
from typing import Dict, Any

from domain.interfaces import IStorageRepository
from domain.schemas import ProcessExtraction

Base = declarative_base()

class ProcessExtractionModel(Base):
    __tablename__ = "process_extractions"

    case_id: Mapped[str] = mapped_column(String, primary_key=True)
    resume: Mapped[str] = mapped_column(String)
    timeline: Mapped[Dict[str, Any]] = mapped_column(JSON)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON)
    persisted_at: Mapped[datetime] = mapped_column(DateTime)

class SqliteRepository(IStorageRepository):
    def __init__(self):
        db_path = os.getenv("SQLITE_DB_PATH", "process_handler.db")
        self.engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def initialize(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_extraction(self, extraction: ProcessExtraction) -> bool:
        try:
            async with self.async_session() as session:
                db_extraction = ProcessExtractionModel(
                    case_id=extraction.case_id,
                    resume=extraction.resume,
                    timeline=[event.model_dump() for event in extraction.timeline],
                    evidence=[evidence.model_dump() for evidence in extraction.evidence],
                    persisted_at=extraction.persisted_at
                )
                session.add(db_extraction)
                await session.commit()
                return True
        except Exception as e:
            print(f"Error saving extraction: {e}")
            return False

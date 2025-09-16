from abc import ABC, abstractmethod
from typing import BinaryIO

from domain.schemas import ProcessExtraction


class ILlmClient(ABC):
    @abstractmethod
    async def analyze_pdf(self, pdf_content: BinaryIO) -> ProcessExtraction:
        """Analyze PDF content using LLM and return structured data"""
        pass


class IStorageRepository(ABC):
    @abstractmethod
    async def save_extraction(self, extraction: ProcessExtraction) -> bool:
        """Save process extraction to storage"""
        pass


class IPdfDownloader(ABC):
    @abstractmethod
    async def download_pdf(self, url: str) -> BinaryIO:
        """Download PDF from URL"""
        pass

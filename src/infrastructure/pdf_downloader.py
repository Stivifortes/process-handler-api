from typing import BinaryIO
import httpx
from io import BytesIO

from domain.interfaces import IPdfDownloader


class PdfDownloader(IPdfDownloader):
    async def download_pdf(self, url: str) -> BinaryIO:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return BytesIO(response.content)

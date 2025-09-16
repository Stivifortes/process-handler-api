from typing import Optional
from pydantic import BaseModel


class ExtractProcessRequest(BaseModel):
    pdf_url: str
    case_id: str

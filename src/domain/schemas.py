from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class TimelineEvent(BaseModel):
    event_id: int
    event_name: str
    event_description: str
    event_date: str
    event_page_init: int
    event_page_end: int

class Evidence(BaseModel):
    evidence_id: int
    evidence_name: str
    evidence_flaw: Optional[str] = None
    evidence_page_init: int
    evidence_page_end: int

class ProcessExtraction(BaseModel):
    case_id: str
    resume: str
    timeline: List[TimelineEvent]
    evidence: List[Evidence]
    persisted_at: datetime = Field(default_factory=datetime.utcnow)

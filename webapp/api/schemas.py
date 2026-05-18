from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    dataset_id: str
    dataset_title: str
    assessed_by: Optional[str] = None
    notes: Optional[str] = None


class IndicatorScoreIn(BaseModel):
    indicator_id: str
    compliance: str
    evidence: Optional[str] = None
    action_notes: Optional[str] = None


class IndicatorScoreOut(BaseModel):
    indicator_id: str
    compliance: str
    evidence: Optional[str] = None
    action_notes: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssessmentOut(BaseModel):
    id: str
    dataset_id: str
    dataset_title: str
    assessed_by: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    scores: list[IndicatorScoreOut] = []
    overall_score: float = 0.0
    f_score: float = 0.0
    a_score: float = 0.0
    i_score: float = 0.0
    r_score: float = 0.0

    class Config:
        from_attributes = True

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String, nullable=False)
    dataset_title = Column(String, nullable=False)
    assessed_by = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scores = relationship(
        "IndicatorScore",
        back_populates="assessment",
        cascade="all, delete-orphan",
    )


class IndicatorScore(Base):
    __tablename__ = "indicator_scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("assessments.id"), nullable=False)
    indicator_id = Column(String, nullable=False)
    compliance = Column(String, default="not_assessed")  # matches ComplianceScore values
    evidence = Column(Text, nullable=True)
    action_notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="scores")

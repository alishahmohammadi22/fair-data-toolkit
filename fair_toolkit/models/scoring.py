"""
FAIR scoring models and result containers.

Provides typed data structures for:
  - IndicatorScore: a single RDA indicator assessment
  - FAIRDimensionScore: aggregated score for one FAIR dimension (F/A/I/R)
  - FAIRAssessmentResult: full assessment output for one dataset
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

from fair_toolkit.models.rda_indicators import (
    FAIRPrinciple,
    ComplianceScore,
    EvidenceLevel,
    SCORE_WEIGHT,
    RDAIndicator,
)


class IndicatorScore(BaseModel):
    indicator_id: str
    indicator_name: str
    principle: FAIRPrinciple
    priority: EvidenceLevel
    compliance: ComplianceScore = ComplianceScore.NOT_ASSESSED
    evidence: Optional[str] = Field(
        default=None,
        description="What evidence was used to determine this score",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Assessor notes, recommendations, or caveats",
    )

    @property
    def numeric_score(self) -> float:
        return SCORE_WEIGHT.get(self.compliance, 0.0)

    @property
    def is_assessed(self) -> bool:
        return self.compliance not in (
            ComplianceScore.NOT_ASSESSED,
            ComplianceScore.NOT_APPLICABLE,
        )


class FAIRDimensionScore(BaseModel):
    principle: FAIRPrinciple
    indicator_scores: list[IndicatorScore]

    @property
    def total_indicators(self) -> int:
        return len(self.indicator_scores)

    @property
    def assessed_indicators(self) -> int:
        return sum(1 for s in self.indicator_scores if s.is_assessed)

    @property
    def compliant_count(self) -> int:
        return sum(
            1 for s in self.indicator_scores
            if s.compliance == ComplianceScore.COMPLIANT
        )

    @property
    def raw_score(self) -> float:
        """Sum of numeric scores for assessed indicators."""
        return sum(s.numeric_score for s in self.indicator_scores if s.is_assessed)

    @property
    def max_score(self) -> float:
        """Maximum possible score (all assessed indicators fully compliant)."""
        return float(self.assessed_indicators)

    @property
    def percentage(self) -> float:
        """0–100 % FAIR score for this dimension."""
        if self.max_score == 0:
            return 0.0
        return round((self.raw_score / self.max_score) * 100, 1)

    @property
    def essential_compliance(self) -> float:
        """% of ESSENTIAL indicators that are compliant."""
        essentials = [
            s for s in self.indicator_scores
            if s.priority == EvidenceLevel.ESSENTIAL and s.is_assessed
        ]
        if not essentials:
            return 0.0
        compliant = sum(1 for s in essentials if s.compliance == ComplianceScore.COMPLIANT)
        return round((compliant / len(essentials)) * 100, 1)


class FAIRAssessmentResult(BaseModel):
    dataset_id: str = Field(description="Identifier for the assessed dataset")
    dataset_title: str
    assessed_by: Optional[str] = None
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
    assessment_method: str = Field(
        default="manual",
        description="'manual' | 'semi-automated' | 'automated'",
    )
    notes: Optional[str] = None

    f_score: FAIRDimensionScore
    a_score: FAIRDimensionScore
    i_score: FAIRDimensionScore
    r_score: FAIRDimensionScore

    @model_validator(mode="after")
    def _check_principles(self) -> FAIRAssessmentResult:
        assert self.f_score.principle == FAIRPrinciple.F
        assert self.a_score.principle == FAIRPrinciple.A
        assert self.i_score.principle == FAIRPrinciple.I
        assert self.r_score.principle == FAIRPrinciple.R
        return self

    @property
    def overall_score(self) -> float:
        """Mean of the four dimension percentages (0–100 %)."""
        scores = [
            self.f_score.percentage,
            self.a_score.percentage,
            self.i_score.percentage,
            self.r_score.percentage,
        ]
        return round(sum(scores) / 4, 1)

    @property
    def dimension_scores(self) -> dict[str, float]:
        return {
            "F": self.f_score.percentage,
            "A": self.a_score.percentage,
            "I": self.i_score.percentage,
            "R": self.r_score.percentage,
            "Overall": self.overall_score,
        }

    @property
    def total_assessed(self) -> int:
        return (
            self.f_score.assessed_indicators
            + self.a_score.assessed_indicators
            + self.i_score.assessed_indicators
            + self.r_score.assessed_indicators
        )

    def get_gaps(self, priority: EvidenceLevel = EvidenceLevel.ESSENTIAL) -> list[IndicatorScore]:
        """Return all non-compliant indicators at or above the given priority level."""
        gaps = []
        priority_order = {
            EvidenceLevel.ESSENTIAL: 0,
            EvidenceLevel.IMPORTANT: 1,
            EvidenceLevel.USEFUL: 2,
        }
        threshold = priority_order[priority]
        for dim in (self.f_score, self.a_score, self.i_score, self.r_score):
            for s in dim.indicator_scores:
                if (
                    priority_order.get(s.priority, 99) <= threshold
                    and s.is_assessed
                    and s.compliance != ComplianceScore.COMPLIANT
                ):
                    gaps.append(s)
        return sorted(gaps, key=lambda x: priority_order.get(x.priority, 99))

    def summary_dict(self) -> dict:
        return {
            "dataset_id": self.dataset_id,
            "dataset_title": self.dataset_title,
            "assessed_at": self.assessed_at.isoformat(),
            "assessment_method": self.assessment_method,
            "F_score_%": self.f_score.percentage,
            "A_score_%": self.a_score.percentage,
            "I_score_%": self.i_score.percentage,
            "R_score_%": self.r_score.percentage,
            "overall_score_%": self.overall_score,
            "total_assessed": self.total_assessed,
            "essential_gaps": len(
                self.get_gaps(EvidenceLevel.ESSENTIAL)
            ),
        }

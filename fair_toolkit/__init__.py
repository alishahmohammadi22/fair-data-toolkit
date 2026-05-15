"""
fair_toolkit — FAIR Data Maturity Assessment Toolkit

Implements the RDA FAIR Maturity Model (41 indicators) and the
Pistoia Alliance FAIR Maturity Matrix (Bronze/Silver/Gold/Platinum)
for assessing and scoring FAIR data in pharmaceutical R&D contexts.
"""

from fair_toolkit.models.rda_indicators import (
    FAIRPrinciple,
    FAIRSubPrinciple,
    IndicatorScope,
    EvidenceLevel,
    RDAIndicator,
    RDA_INDICATORS,
)
from fair_toolkit.models.pistoia_matrix import (
    MaturityLevel,
    PistoiaIndicator,
    PISTOIA_MATRIX,
)
from fair_toolkit.models.scoring import (
    IndicatorScore,
    FAIRDimensionScore,
    FAIRAssessmentResult,
)
from fair_toolkit.assessors.manual_assessor import ManualFAIRAssessor

__version__ = "0.1.0"
__all__ = [
    "FAIRPrinciple",
    "FAIRSubPrinciple",
    "IndicatorScope",
    "EvidenceLevel",
    "RDAIndicator",
    "RDA_INDICATORS",
    "MaturityLevel",
    "PistoiaIndicator",
    "PISTOIA_MATRIX",
    "IndicatorScore",
    "FAIRDimensionScore",
    "FAIRAssessmentResult",
    "ManualFAIRAssessor",
]

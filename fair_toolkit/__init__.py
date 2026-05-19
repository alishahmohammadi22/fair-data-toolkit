"""
fair_toolkit — FAIR Data Maturity Assessment Toolkit

Implements the RDA FAIR Maturity Model (41 indicators) and the
Pistoia Alliance FAIR Maturity Matrix (L0–L5 × 7 organisational dimensions)
for assessing and scoring FAIR data in pharmaceutical R&D contexts.
"""

from fair_toolkit.models.rda_indicators import (
    FAIRPrinciple,
    FAIRSubPrinciple,
    IndicatorScope,
    EvidenceLevel,
    ComplianceScore,
    RDAIndicator,
    RDA_INDICATORS,
    get_indicators_by_principle,
    get_indicators_by_priority,
    get_indicator,
)
from fair_toolkit.models.pistoia_matrix import (
    MaturityLevel,
    MatrixDimension,
    MatrixCell,
    PISTOIA_MATRIX,
    LEVEL_METADATA,
    get_cell,
    get_level_cells,
    get_dimension_cells,
    describe_level,
)
from fair_toolkit.models.scoring import (
    IndicatorScore,
    FAIRDimensionScore,
    FAIRAssessmentResult,
)
from fair_toolkit.assessors.manual_assessor import ManualFAIRAssessor

__version__ = "0.2.0"
__all__ = [
    "FAIRPrinciple",
    "FAIRSubPrinciple",
    "IndicatorScope",
    "EvidenceLevel",
    "ComplianceScore",
    "RDAIndicator",
    "RDA_INDICATORS",
    "get_indicators_by_principle",
    "get_indicators_by_priority",
    "get_indicator",
    "MaturityLevel",
    "MatrixDimension",
    "MatrixCell",
    "PISTOIA_MATRIX",
    "LEVEL_METADATA",
    "get_cell",
    "get_level_cells",
    "get_dimension_cells",
    "describe_level",
    "IndicatorScore",
    "FAIRDimensionScore",
    "FAIRAssessmentResult",
    "ManualFAIRAssessor",
]

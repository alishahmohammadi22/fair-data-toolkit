"""Tests for RDA FAIR Maturity Model indicators and scoring."""
import pytest
from fair_toolkit import (
    RDA_INDICATORS, FAIRPrinciple, EvidenceLevel, IndicatorScope,
    ComplianceScore, ManualFAIRAssessor,
    get_indicators_by_principle, get_indicator,
)


class TestRDAIndicators:
    def test_total_count(self):
        assert len(RDA_INDICATORS) == 41

    def test_all_principles_present(self):
        principles = {ind.principle for ind in RDA_INDICATORS}
        assert principles == {FAIRPrinciple.F, FAIRPrinciple.A, FAIRPrinciple.I, FAIRPrinciple.R}

    def test_findable_count(self):
        f_inds = get_indicators_by_principle(FAIRPrinciple.F)
        assert len(f_inds) == 7

    def test_get_indicator_by_id(self):
        ind = get_indicator("RDA-F1-01D")
        assert ind is not None
        assert ind.principle == FAIRPrinciple.F
        assert ind.scope == IndicatorScope.DATA

    def test_get_indicator_not_found(self):
        assert get_indicator("RDA-X9-99Z") is None

    def test_all_ids_unique(self):
        ids = [ind.id for ind in RDA_INDICATORS]
        assert len(ids) == len(set(ids))

    def test_essential_indicators_present(self):
        essential = [ind for ind in RDA_INDICATORS if ind.priority == EvidenceLevel.ESSENTIAL]
        assert len(essential) > 0

    def test_indicator_has_required_fields(self):
        ind = get_indicator("RDA-F2-01M")
        assert ind.id
        assert ind.name
        assert ind.question


class TestManualAssessor:
    def setup_method(self):
        self.assessor = ManualFAIRAssessor(
            dataset_id="TEST-001",
            dataset_title="Test Dataset",
            assessed_by="Test",
        )

    def test_initial_progress(self):
        prog = self.assessor.progress()
        assert prog["total"] == 41
        assert prog["assessed"] == 0
        assert prog["remaining"] == 41

    def test_score_indicator(self):
        self.assessor.score("RDA-F1-01D", ComplianceScore.COMPLIANT, evidence="DOI assigned")
        prog = self.assessor.progress()
        assert prog["assessed"] == 1

    def test_mark_not_applicable(self):
        self.assessor.mark_not_applicable("RDA-A1.1-01M", reason="Not externally accessible")
        prog = self.assessor.progress()
        assert prog["assessed"] == 1

    def test_build_result_partial(self):
        self.assessor.score("RDA-F1-01D", ComplianceScore.COMPLIANT)
        self.assessor.score("RDA-F1-01M", ComplianceScore.NOT_COMPLIANT)
        result = self.assessor.build_result()
        assert result is not None
        assert result.overall_score >= 0

    def test_score_batch(self):
        batch = {
            "RDA-F1-01D": ComplianceScore.COMPLIANT,
            "RDA-F1-01M": ComplianceScore.PARTIALLY_COMPLIANT,
            "RDA-F2-01M": ComplianceScore.NOT_COMPLIANT,
        }
        self.assessor.score_batch(batch)
        assert self.assessor.progress()["assessed"] == 3

    def test_unassessed_list(self):
        self.assessor.score("RDA-F1-01D", ComplianceScore.COMPLIANT)
        unassessed = self.assessor.unassessed()
        assert "RDA-F1-01D" not in unassessed
        assert len(unassessed) == 40


class TestScoringLogic:
    def test_compliant_score_is_1(self):
        assessor = ManualFAIRAssessor("DS-001", "Test", "Test")
        assessor.score("RDA-F1-01D", ComplianceScore.COMPLIANT)
        result = assessor.build_result()
        ind_score = next(s for s in result.f_score.indicator_scores if s.indicator_id == "RDA-F1-01D")
        assert ind_score.numeric_score == 1.0

    def test_partial_score_is_half(self):
        assessor = ManualFAIRAssessor("DS-001", "Test", "Test")
        assessor.score("RDA-F1-01D", ComplianceScore.PARTIALLY_COMPLIANT)
        result = assessor.build_result()
        ind_score = next(s for s in result.f_score.indicator_scores if s.indicator_id == "RDA-F1-01D")
        assert ind_score.numeric_score == 0.5

    def test_not_compliant_score_is_0(self):
        assessor = ManualFAIRAssessor("DS-001", "Test", "Test")
        assessor.score("RDA-F1-01D", ComplianceScore.NOT_COMPLIANT)
        result = assessor.build_result()
        ind_score = next(s for s in result.f_score.indicator_scores if s.indicator_id == "RDA-F1-01D")
        assert ind_score.numeric_score == 0.0

    def test_not_applicable_excluded_from_score(self):
        assessor = ManualFAIRAssessor("DS-001", "Test", "Test")
        assessor.mark_not_applicable("RDA-F1-01D", "N/A for this data type")
        result = assessor.build_result()
        ind_score = next(s for s in result.f_score.indicator_scores if s.indicator_id == "RDA-F1-01D")
        assert not ind_score.is_assessed

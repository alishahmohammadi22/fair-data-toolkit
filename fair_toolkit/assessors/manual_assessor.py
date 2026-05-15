"""
ManualFAIRAssessor — interactive tool for conducting a manual RDA FAIR assessment.

Usage:
    assessor = ManualFAIRAssessor(dataset_id="DS-001", dataset_title="My Dataset")

    # Score individual indicators
    assessor.score("RDA-F1-01D", ComplianceScore.COMPLIANT, evidence="DOI 10.5281/zenodo.xxx")
    assessor.score("RDA-F1-02D", ComplianceScore.COMPLIANT)
    assessor.score("RDA-A1-01M", ComplianceScore.PARTIALLY_COMPLIANT, notes="Access process exists but undocumented")

    # Get the full result
    result = assessor.build_result()
    print(result.overall_score)         # e.g. 72.5
    print(result.dimension_scores)      # {"F": 80.0, "A": 60.0, "I": 75.0, "R": 74.0, "Overall": 72.5}
"""

from __future__ import annotations
from typing import Optional
from pydantic import ValidationError

from fair_toolkit.models.rda_indicators import (
    FAIRPrinciple,
    EvidenceLevel,
    ComplianceScore,
    RDAIndicator,
    RDA_INDICATORS,
    get_indicator,
)
from fair_toolkit.models.scoring import (
    IndicatorScore,
    FAIRDimensionScore,
    FAIRAssessmentResult,
)


class ManualFAIRAssessor:
    """
    Walk through all 41 RDA FAIR indicators and record compliance scores.

    The assessor holds a mutable dictionary of IndicatorScore objects,
    all initialised to NOT_ASSESSED. Call `.score()` to update individual
    indicators, then call `.build_result()` to get the final scored object.
    """

    def __init__(
        self,
        dataset_id: str,
        dataset_title: str,
        assessed_by: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        self.dataset_id = dataset_id
        self.dataset_title = dataset_title
        self.assessed_by = assessed_by
        self.notes = notes

        # Pre-populate all indicators as NOT_ASSESSED
        self._scores: dict[str, IndicatorScore] = {
            ind.id: IndicatorScore(
                indicator_id=ind.id,
                indicator_name=ind.name,
                principle=ind.principle,
                priority=ind.priority,
                compliance=ComplianceScore.NOT_ASSESSED,
            )
            for ind in RDA_INDICATORS
        }

    # ── Scoring API ────────────────────────────────────────────────────────

    def score(
        self,
        indicator_id: str,
        compliance: ComplianceScore,
        evidence: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Record a compliance score for a single RDA indicator."""
        if indicator_id not in self._scores:
            raise ValueError(
                f"Unknown indicator ID: '{indicator_id}'. "
                f"Valid IDs: {sorted(self._scores.keys())[:5]}..."
            )
        self._scores[indicator_id] = self._scores[indicator_id].model_copy(
            update={
                "compliance": compliance,
                "evidence": evidence,
                "notes": notes,
            }
        )

    def mark_not_applicable(self, indicator_id: str, reason: Optional[str] = None) -> None:
        """Mark an indicator as not applicable (e.g., A1.2 for fully open datasets)."""
        self.score(indicator_id, ComplianceScore.NOT_APPLICABLE, notes=reason)

    def score_batch(self, scores: dict[str, ComplianceScore]) -> None:
        """Score multiple indicators at once. keys = indicator IDs, values = ComplianceScore."""
        for indicator_id, compliance in scores.items():
            self.score(indicator_id, compliance)

    # ── Status helpers ─────────────────────────────────────────────────────

    def unassessed(self) -> list[str]:
        """Return IDs of indicators not yet assessed."""
        return [
            k for k, v in self._scores.items()
            if v.compliance == ComplianceScore.NOT_ASSESSED
        ]

    def progress(self) -> dict[str, int]:
        """Return assessment progress counts."""
        assessed = sum(1 for v in self._scores.values() if v.is_assessed)
        total = len(self._scores)
        return {
            "assessed": assessed,
            "total": total,
            "remaining": total - assessed,
            "pct_complete": round((assessed / total) * 100, 1),
        }

    def get_indicators_by_principle(self, principle: FAIRPrinciple) -> list[tuple[RDAIndicator, IndicatorScore]]:
        """Return (indicator, score) pairs for a given FAIR principle."""
        result = []
        for ind in RDA_INDICATORS:
            if ind.principle == principle:
                result.append((ind, self._scores[ind.id]))
        return result

    # ── Build result ───────────────────────────────────────────────────────

    def build_result(self) -> FAIRAssessmentResult:
        """Compile all scored indicators into a FAIRAssessmentResult."""

        def _dim(principle: FAIRPrinciple) -> FAIRDimensionScore:
            return FAIRDimensionScore(
                principle=principle,
                indicator_scores=[
                    self._scores[ind.id]
                    for ind in RDA_INDICATORS
                    if ind.principle == principle
                ],
            )

        return FAIRAssessmentResult(
            dataset_id=self.dataset_id,
            dataset_title=self.dataset_title,
            assessed_by=self.assessed_by,
            notes=self.notes,
            assessment_method="manual",
            f_score=_dim(FAIRPrinciple.F),
            a_score=_dim(FAIRPrinciple.A),
            i_score=_dim(FAIRPrinciple.I),
            r_score=_dim(FAIRPrinciple.R),
        )

    # ── Pretty print helpers (Rich) ────────────────────────────────────────

    def print_scorecard(self) -> None:
        """Print a formatted score card to the terminal using Rich (if available)."""
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.text import Text
        except ImportError:
            print("Install 'rich' for formatted output: pip install rich")
            result = self.build_result()
            for dim, score in result.dimension_scores.items():
                print(f"  {dim}: {score}%")
            return

        console = Console()
        result = self.build_result()

        table = Table(title=f"FAIR Assessment — {self.dataset_title}", show_lines=True)
        table.add_column("Dimension", style="bold")
        table.add_column("Score", justify="right")
        table.add_column("Essential %", justify="right")
        table.add_column("Assessed / Total", justify="right")

        colours = {"F": "blue", "A": "green", "I": "magenta", "R": "yellow"}
        for principle, dim_score in [
            ("F", result.f_score),
            ("A", result.a_score),
            ("I", result.i_score),
            ("R", result.r_score),
        ]:
            colour = colours[principle]
            table.add_row(
                Text(f"[{principle}] {FAIRPrinciple[principle].name}", style=colour),
                f"[bold]{dim_score.percentage}%[/bold]",
                f"{dim_score.essential_compliance}%",
                f"{dim_score.assessed_indicators} / {dim_score.total_indicators}",
            )

        table.add_row(
            "[bold white]OVERALL[/bold white]",
            f"[bold white]{result.overall_score}%[/bold white]",
            "",
            f"{result.total_assessed} / {len(RDA_INDICATORS)}",
        )
        console.print(table)

        gaps = result.get_gaps(EvidenceLevel.ESSENTIAL)
        if gaps:
            console.print(
                f"\n[red bold]{len(gaps)} essential gap(s) requiring attention:[/red bold]"
            )
            for g in gaps:
                console.print(f"  [red]✗[/red] {g.indicator_id} — {g.indicator_name}")
        else:
            console.print("\n[green bold]✓ All essential indicators are compliant.[/green bold]")

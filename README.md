# fair-data-toolkit

**FAIR Data Maturity Framework for Pharmaceutical R&D**  
*From RDA indicators to agentic AI scoring*

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-informational)](https://alishahmohammadi22.github.io/fair-data-toolkit)

---

## Overview

`fair-data-toolkit` is a Python package and article series that provides a structured, measurable approach to FAIR data maturity in pharmaceutical and life sciences organisations.

It implements two complementary frameworks:

- **RDA FAIR Maturity Model (2020)** — 41 indicators across F/A/I/R with Essential / Important / Useful priority levels  
- **Pistoia Alliance FAIR Maturity Matrix** — Bronze / Silver / Gold / Platinum tiered model for pharma

The toolkit enables you to conduct a full manual FAIR assessment, score all 41 indicators, generate a gap analysis, and build a prioritised remediation roadmap.

---

## Article Series

| # | Article | Description |
|---|---------|-------------|
| 01 | [Introduction to FAIR Data Principles](notebooks/01_introduction_to_fair.ipynb) | The 15 FAIR sub-principles, FAIR vs Open, pharma context, key stakeholders |
| 02 | [RDA FAIR Maturity Model](notebooks/02_rda_fair_maturity_model.ipynb) | All 41 RDA indicators, scoring system, worked gap analysis |
| 03 | [Pistoia Alliance FAIR Maturity Matrix](notebooks/03_pistoia_fair_maturity_matrix.ipynb) | Bronze/Silver/Gold/Platinum tiers, pharma mapping, org assessment |
| 04 | [Manual FAIR Assessment Walkthrough](notebooks/04_manual_fair_assessment_walkthrough.ipynb) | Full assessment of a CAR-T viability dataset, export, remediation roadmap |
| 05 | [FAIR Score Calculator](notebooks/05_fair_score_calculator.ipynb) | Semi-automated scoring from Zenodo API; agentic scorer architecture sketch |

> **Coming next:** `fair_agent/` — a LangGraph + GPT agentic system that scores all 41 RDA indicators given any database REST API endpoint.

---

## Installation

```bash
pip install fair-data-toolkit
```

With notebook dependencies:

```bash
pip install "fair-data-toolkit[notebooks]"
```

From source:

```bash
git clone https://github.com/alishahmohammadi22/fair-data-toolkit.git
cd fair-data-toolkit
pip install -e ".[notebooks]"
```

---

## Quick Start

```python
from fair_toolkit import ManualFAIRAssessor, ComplianceScore

# Initialise an assessment
assessor = ManualFAIRAssessor(
    dataset_id="DS-001",
    dataset_title="CAR-T Cell Viability Assay",
    assessed_by="Ali Shahmohammadi",
)

# Score indicators
assessor.score("RDA-F1-01D", ComplianceScore.NOT_COMPLIANT,
               evidence="Only internal LIMS ID, no global PID")
assessor.score("RDA-F2-01M", ComplianceScore.PARTIALLY_COMPLIANT,
               evidence="Basic metadata present; assay conditions missing")
assessor.score("RDA-A1.2-01M", ComplianceScore.COMPLIANT,
               evidence="Azure AD OAuth 2.0 controls access")

# Generate scorecard
assessor.print_scorecard()

# Build result and analyse gaps
result = assessor.build_result()
print(f"Overall FAIR score: {result.overall_score}%")

essential_gaps = result.get_gaps(EvidenceLevel.ESSENTIAL)
for gap in essential_gaps:
    print(f"  ✗ {gap.indicator_id}: {gap.indicator_name}")
```

---

## Package Structure

```
fair_toolkit/
├── models/
│   ├── rda_indicators.py    # All 41 RDA FAIR Maturity Model indicators
│   ├── pistoia_matrix.py    # Pistoia Alliance Bronze/Silver/Gold/Platinum matrix
│   └── scoring.py           # IndicatorScore, FAIRDimensionScore, FAIRAssessmentResult
└── assessors/
    └── manual_assessor.py   # ManualFAIRAssessor — interactive assessment tool
```

### Key Classes

**`ManualFAIRAssessor`**  
Full manual assessment workflow. Score indicators one by one or in batch, print a rich scorecard, and export the result.

**`FAIRAssessmentResult`**  
Container for a complete assessment. Holds dimension scores for F/A/I/R, calculates the overall score, and provides gap analysis by priority level.

**`RDA_INDICATORS`**  
List of all 41 `RDAIndicator` objects with id, principle, sub-principle, scope, priority, question, guidance, and examples.

**`PISTOIA_MATRIX`**  
List of all `PistoiaIndicator` objects spanning Bronze through Platinum, with links to corresponding RDA indicators and pharma-specific context.

---

## FAIR Frameworks Implemented

### RDA FAIR Maturity Model (2020)

| Dimension | Indicators | Priority breakdown |
|-----------|------------|-------------------|
| Findable | 7 | 4 Essential, 2 Important, 1 Useful |
| Accessible | 9 | 3 Essential, 4 Important, 2 Useful |
| Interoperable | 12 | 2 Essential, 6 Important, 4 Useful |
| Reusable | 13 | 3 Essential, 7 Important, 3 Useful |
| **Total** | **41** | **12 Essential, 19 Important, 10 Useful** |

Compliance levels: `Not Applicable` / `Not Assessed` / `Not Compliant` / `Partially Compliant` / `Compliant`

### Pistoia Alliance FAIR Maturity Matrix

| Level | Focus |
|-------|-------|
| 🥉 Bronze | Awareness: internal IDs, basic metadata, documented access |
| 🥈 Silver | Standards: global PIDs, controlled vocabularies, open APIs |
| 🥇 Gold | Automation: machine-readable metadata, automated validation, FAIR scores tracked |
| 💎 Platinum | Self-service: FAIR-by-design, cross-org interoperability, continuous improvement |

---

## Roadmap

### Phase 1 — Manual Assessment Toolkit (this release)
- [x] All 41 RDA FAIR Maturity Model indicators as Pydantic models
- [x] Pistoia Alliance FAIR Maturity Matrix (Bronze → Platinum)
- [x] `ManualFAIRAssessor` with Rich scorecard output
- [x] Gap analysis by priority level
- [x] 5-article Jupyter notebook series

### Phase 2 — Agentic FAIR Scorer (`fair_agent/`)
- [ ] `MetadataFetcherAgent` — fetches and parses metadata from any REST API
- [ ] `StructuralAssessorAgent` — auto-scores ~20 structural indicators
- [ ] `ContentAnalysisAgent` (GPT) — scores semantic/content indicators
- [ ] `ExternalVerifierAgent` — validates ontology terms via BioPortal/OLS
- [ ] `GovernanceReporterAgent` — compiles result and routes gaps for human review
- [ ] Full LangGraph pipeline — accepts any API endpoint, returns `FAIRAssessmentResult`

---

## References

- Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18
- RDA FAIR Data Maturity Model Working Group (2020). FAIR Data Maturity Model: specification and guidelines. https://doi.org/10.15497/rda00050
- Pistoia Alliance (2021). FAIR Data Implementation Profile for Life Sciences. https://www.pistoiaalliance.org/projects/current-projects/fair-data/

---

## License

MIT License — see [LICENSE](LICENSE)

---

*Developed by Ali Shahmohammadi, Ph.D. — Takeda Pharmaceutical*

"""
Pistoia Alliance FAIR Maturity Matrix.

The Pistoia Alliance FAIR Maturity Matrix provides a tiered, pragmatic
framework specifically designed for pharmaceutical and life sciences
organisations. Each tier (Bronze → Silver → Gold → Platinum) maps to
progressively higher FAIR compliance and automation.

Source: Pistoia Alliance FAIR Data Working Group
        https://www.pistoiaalliance.org/projects/current-projects/fair-data/
"""

from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MaturityLevel(str, Enum):
    BRONZE = "bronze"       # Level 1 — Awareness & initial implementation
    SILVER = "silver"       # Level 2 — Defined processes & metadata standards
    GOLD = "gold"           # Level 3 — Automated assessment & compliance
    PLATINUM = "platinum"   # Level 4 — Self-service FAIR with continuous improvement


LEVEL_DESCRIPTIONS: dict[MaturityLevel, str] = {
    MaturityLevel.BRONZE: (
        "Organisation is aware of FAIR principles and has begun identifying gaps. "
        "Metadata is captured manually and inconsistently. Data is findable within "
        "the organisation but not externally. No automated FAIR assessment in place."
    ),
    MaturityLevel.SILVER: (
        "Defined metadata schemas and controlled vocabularies are in place for key data types. "
        "PIDs are assigned to major datasets. Data is accessible via documented APIs. "
        "Community standards adopted for at least one primary data domain. "
        "Manual FAIR assessments conducted periodically."
    ),
    MaturityLevel.GOLD: (
        "FAIR assessment is automated or semi-automated. Metadata is machine-readable "
        "and validated against schemas. Ontology-based metadata is standard practice. "
        "Provenance is captured systematically. FAIR scores tracked over time. "
        "External discoverability established for key datasets."
    ),
    MaturityLevel.PLATINUM: (
        "FAIR by design: all new data is automatically assessed at ingestion. "
        "Continuous improvement loops driven by FAIR score metrics. "
        "Data interoperable across organisational and domain boundaries. "
        "Full provenance, ALCOA+ compliance, and machine-actionable governance. "
        "Contributing to cross-industry FAIR standards development."
    ),
}


class PistoiaIndicator(BaseModel):
    id: str = Field(description="Unique Pistoia indicator ID, e.g. 'PA-F-B1'")
    dimension: str = Field(description="FAIR dimension: F, A, I, or R")
    level: MaturityLevel
    name: str
    criterion: str = Field(description="What must be true for this level to be met")
    rda_indicator_ids: list[str] = Field(
        default_factory=list,
        description="Corresponding RDA FAIR Maturity indicator IDs",
    )
    pharma_context: Optional[str] = Field(
        default=None,
        description="Pharmaceutical/life sciences specific guidance",
    )


PISTOIA_MATRIX: list[PistoiaIndicator] = [

    # ═══════════════════════════════════════════════════════════════════════
    # FINDABLE
    # ═══════════════════════════════════════════════════════════════════════

    PistoiaIndicator(
        id="PA-F-B1",
        dimension="F",
        level=MaturityLevel.BRONZE,
        name="Datasets have internal identifiers",
        criterion=(
            "Every dataset has a locally unique identifier within the organisation's "
            "systems (e.g., LIMS ID, ELN experiment number, study ID)."
        ),
        rda_indicator_ids=["RDA-F1-01D", "RDA-F1-01M"],
        pharma_context=(
            "Most pharma organisations already assign study IDs (e.g., STD-2024-001). "
            "Bronze is about confirming these are systematically captured and searchable "
            "within the organisation — not yet globally unique."
        ),
    ),
    PistoiaIndicator(
        id="PA-F-B2",
        dimension="F",
        level=MaturityLevel.BRONZE,
        name="Basic metadata captured for all datasets",
        criterion=(
            "A minimum metadata set is captured for all new datasets: "
            "title, creator, date created, data type, project association, and internal location."
        ),
        rda_indicator_ids=["RDA-F2-01M"],
        pharma_context=(
            "This maps to minimum required fields in an ELN (Benchling, LabArchives) "
            "or LIMS (LabKey, Veeva Vault). Bronze does not require community standard "
            "compliance — just consistent internal capture."
        ),
    ),
    PistoiaIndicator(
        id="PA-F-S1",
        dimension="F",
        level=MaturityLevel.SILVER,
        name="Global persistent identifiers assigned to key datasets",
        criterion=(
            "Datasets that may be shared externally (publications, regulatory submissions, "
            "collaborations) are assigned DOIs or equivalent global PIDs via a repository."
        ),
        rda_indicator_ids=["RDA-F1-01D", "RDA-F1-02D", "RDA-F1-01M", "RDA-F1-02M"],
        pharma_context=(
            "Typical repositories: Zenodo, Figshare, ChEMBL (chemistry), EBI repositories, "
            "FDA data repositories. Not every internal dataset needs a global PID at Silver — "
            "focus on externally shareable datasets first."
        ),
    ),
    PistoiaIndicator(
        id="PA-F-S2",
        dimension="F",
        level=MaturityLevel.SILVER,
        name="Metadata searchable in an external index",
        criterion=(
            "Metadata for externally shared datasets is registered in at least one "
            "searchable external index or data catalogue (DataCite, Google Dataset Search, "
            "FAIRsharing, a domain repository)."
        ),
        rda_indicator_ids=["RDA-F4-01M"],
        pharma_context=(
            "For pre-competitive pharma data: ChEMBL, BindingDB, PDB. "
            "For clinical: ClinicalTrials.gov, CSDR, YODA Project. "
            "For internal discoverability: an enterprise data catalogue (Collibra, Alation, Azure Purview)."
        ),
    ),
    PistoiaIndicator(
        id="PA-F-G1",
        dimension="F",
        level=MaturityLevel.GOLD,
        name="Metadata richness validated against domain standard",
        criterion=(
            "Metadata completeness is automatically validated against a domain community "
            "standard at the point of dataset registration. Incomplete submissions are flagged."
        ),
        rda_indicator_ids=["RDA-F2-01M", "RDA-R1.3-01M"],
        pharma_context=(
            "Implement metadata quality gates in ELN/LIMS workflows. "
            "For bioassays: validate against ISA-Tab or MIABI minimum information. "
            "For chemistry: validate against ChEMBL submission standards."
        ),
    ),
    PistoiaIndicator(
        id="PA-F-P1",
        dimension="F",
        level=MaturityLevel.PLATINUM,
        name="FAIR-by-design: metadata auto-generated at data capture",
        criterion=(
            "Metadata is automatically generated and attached to datasets at the point "
            "of data capture from instruments, ELNs, or assay systems — no manual metadata "
            "entry required for standard data types."
        ),
        rda_indicator_ids=["RDA-F2-01M", "RDA-F1-01D", "RDA-F3-01M"],
        pharma_context=(
            "Instrument → ELN → LIMS → data catalogue pipeline with automatic metadata "
            "propagation. Implemented via lab automation middleware or API-driven integration "
            "between LabKey, Benchling, and enterprise data platforms."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # ACCESSIBLE
    # ═══════════════════════════════════════════════════════════════════════

    PistoiaIndicator(
        id="PA-A-B1",
        dimension="A",
        level=MaturityLevel.BRONZE,
        name="Data retrievable by internal request process",
        criterion=(
            "There is a documented process by which colleagues can request access to datasets. "
            "The process is findable from the metadata record or internal catalogue."
        ),
        rda_indicator_ids=["RDA-A1-01M"],
        pharma_context=(
            "Most pharma organisations have a data request form or email process. "
            "Bronze requires that this process is documented and discoverable — "
            "not just known informally within a team."
        ),
    ),
    PistoiaIndicator(
        id="PA-A-S1",
        dimension="A",
        level=MaturityLevel.SILVER,
        name="Data accessible via a documented API",
        criterion=(
            "Key datasets are accessible via a documented REST API or equivalent "
            "programmatic access method. API documentation is publicly available."
        ),
        rda_indicator_ids=["RDA-A1-02M", "RDA-A1-03D", "RDA-A1.1-01D"],
        pharma_context=(
            "LIMS and ELN systems (LabKey, Benchling, Thermo Fisher SampleManager) "
            "typically expose REST APIs. Silver requires that the API is documented, "
            "stable, and known to data consumers — not just technically available."
        ),
    ),
    PistoiaIndicator(
        id="PA-A-S2",
        dimension="A",
        level=MaturityLevel.SILVER,
        name="Access control is standards-based",
        criterion=(
            "Authentication and authorisation for controlled-access datasets "
            "uses a standards-based protocol (OAuth 2.0, SAML, OpenID Connect). "
            "Access decisions are logged."
        ),
        rda_indicator_ids=["RDA-A1.2-01D", "RDA-A1.2-01M"],
        pharma_context=(
            "Enterprise SSO (Azure AD, Okta) satisfies this for internal systems. "
            "For external collaborations: OIDC-based access via a data access committee portal. "
            "Access logs support audit trail requirements (GxP, 21 CFR Part 11)."
        ),
    ),
    PistoiaIndicator(
        id="PA-A-G1",
        dimension="A",
        level=MaturityLevel.GOLD,
        name="Metadata persists after data retirement",
        criterion=(
            "When a dataset is retired, restricted, or deleted, its metadata record "
            "remains accessible with a 'tombstone' record explaining the data status."
        ),
        rda_indicator_ids=["RDA-A2-01M"],
        pharma_context=(
            "Critical for regulatory submissions: FDA and EMA may request data years after "
            "a study closes. Tombstone records with the study ID, data custodian contact, "
            "and archive location are the minimum. CoreTrustSeal-certified repositories provide this."
        ),
    ),
    PistoiaIndicator(
        id="PA-A-P1",
        dimension="A",
        level=MaturityLevel.PLATINUM,
        name="Machine-actionable access control with dynamic permissions",
        criterion=(
            "Access permissions are machine-readable and enforced automatically "
            "based on user role, project membership, and data sensitivity classification. "
            "No manual approval needed for routine access within approved scope."
        ),
        rda_indicator_ids=["RDA-A1.2-01D", "RDA-A1-02M"],
        pharma_context=(
            "Attribute-based access control (ABAC) linked to the data catalogue. "
            "Policy-as-code (e.g., OPA — Open Policy Agent) enforcing data access "
            "rules based on data classification tags applied at ingestion."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # INTEROPERABLE
    # ═══════════════════════════════════════════════════════════════════════

    PistoiaIndicator(
        id="PA-I-B1",
        dimension="I",
        level=MaturityLevel.BRONZE,
        name="Data uses a non-proprietary file format",
        criterion=(
            "Key datasets are stored in or exportable to a non-proprietary, "
            "open file format (CSV, JSON, XML, FASTA, SDF, mzML, etc.)."
        ),
        rda_indicator_ids=["RDA-I1-01D", "RDA-I1-02D"],
        pharma_context=(
            "Many instruments output proprietary binary formats. Bronze requires "
            "that an open-format export is available and preserved alongside the raw data. "
            "E.g., Waters RAW → mzML conversion via ProteoWizard."
        ),
    ),
    PistoiaIndicator(
        id="PA-I-S1",
        dimension="I",
        level=MaturityLevel.SILVER,
        name="Metadata uses controlled vocabularies with PIDs",
        criterion=(
            "Key metadata fields (assay type, organism, cell line, compound, disease) "
            "use terms from a registered ontology or controlled vocabulary that has "
            "persistent identifiers (OBI, ChEBI, CL, NCBITaxon, DOID, MeSH, SNOMED)."
        ),
        rda_indicator_ids=["RDA-I2-01M", "RDA-I2-01D"],
        pharma_context=(
            "Map internal codebooks to OBO Foundry or CDISC terminology. "
            "Register ontology usage on FAIRsharing.org. "
            "Priority fields: assay type (OBI), compound (ChEBI/PubChem), "
            "cell line (Cellosaurus), species (NCBITaxon), disease (DOID/MedDRA)."
        ),
    ),
    PistoiaIndicator(
        id="PA-I-S2",
        dimension="I",
        level=MaturityLevel.SILVER,
        name="Metadata expressed in a structured, machine-readable format",
        criterion=(
            "Metadata is stored and exposed in a structured, machine-readable format "
            "(JSON, JSON-LD, XML with schema, RDF) — not only as free text or PDF."
        ),
        rda_indicator_ids=["RDA-I1-01M", "RDA-I1-02M"],
        pharma_context=(
            "Most modern LIMS/ELN systems support JSON/XML export. "
            "Silver requires that these exports are systematically generated and maintained, "
            "not just technically possible. Check that the exported format validates against a schema."
        ),
    ),
    PistoiaIndicator(
        id="PA-I-G1",
        dimension="I",
        level=MaturityLevel.GOLD,
        name="Data includes cross-references to external resources",
        criterion=(
            "Data files and metadata include typed cross-references to related "
            "external datasets, publications, and resources using resolvable identifiers."
        ),
        rda_indicator_ids=["RDA-I3-01M", "RDA-I3-01D", "RDA-I3-02M"],
        pharma_context=(
            "HTS data referencing ChEMBL compound IDs; gene expression data referencing "
            "Ensembl gene IDs; assay data referencing protocol DOIs from protocols.io. "
            "Implement as standard columns in data exports and structured metadata fields."
        ),
    ),
    PistoiaIndicator(
        id="PA-I-P1",
        dimension="I",
        level=MaturityLevel.PLATINUM,
        name="Data is semantically interoperable across organisational boundaries",
        criterion=(
            "Data can be automatically integrated with datasets from external organisations "
            "or public repositories without manual data transformation, because shared "
            "ontologies, identifiers, and formats are used end-to-end."
        ),
        rda_indicator_ids=["RDA-I1-02M", "RDA-I2-01M", "RDA-I3-01M", "RDA-I3-01D"],
        pharma_context=(
            "TransCelerate, IMI MELLODDY, ATOM Consortium, and Open Targets are examples "
            "of cross-pharma data sharing initiatives where semantic interoperability is required. "
            "Achieving Platinum typically requires adopting shared data models (OMOP CDM, ISA-Tab)."
        ),
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # REUSABLE
    # ═══════════════════════════════════════════════════════════════════════

    PistoiaIndicator(
        id="PA-R-B1",
        dimension="R",
        level=MaturityLevel.BRONZE,
        name="All datasets have an explicit licence or usage terms",
        criterion=(
            "Every dataset has an explicitly stated licence or terms of use. "
            "The licence is findable from the metadata record. "
            "'Internal use only' with a documented scope counts as Bronze."
        ),
        rda_indicator_ids=["RDA-R1.1-01M"],
        pharma_context=(
            "Many pharma datasets default to 'all rights reserved' by omission. "
            "Bronze requires that a conscious licensing decision is made and documented "
            "for every dataset — even if the decision is 'restricted to project team'."
        ),
    ),
    PistoiaIndicator(
        id="PA-R-S1",
        dimension="R",
        level=MaturityLevel.SILVER,
        name="Open datasets use standard open licences",
        criterion=(
            "Datasets intended for external sharing use a well-known standard open licence "
            "(CC BY 4.0, CC0, ODbL). Custom or proprietary licences are replaced with "
            "standard equivalents where legally possible."
        ),
        rda_indicator_ids=["RDA-R1.1-01M", "RDA-R1.1-02M", "RDA-R1.1-03M"],
        pharma_context=(
            "Pre-competitive pharma data shared via TransCelerate or ATOM typically uses CC BY. "
            "Clinical trial data shared via CSDR/YODA may use CC BY with an additional "
            "data use agreement. Work with legal to create standard licence templates."
        ),
    ),
    PistoiaIndicator(
        id="PA-R-S2",
        dimension="R",
        level=MaturityLevel.SILVER,
        name="Provenance captured for all data transformations",
        criterion=(
            "Data processing, transformation, and analysis steps are documented "
            "and linked to the dataset. At minimum: who ran what software version "
            "on what input data, when."
        ),
        rda_indicator_ids=["RDA-R1.2-01M"],
        pharma_context=(
            "Use ELN audit trails, workflow management systems (Nextflow, Snakemake), "
            "or laboratory information systems that capture processing history. "
            "For GxP data: compliant with 21 CFR Part 11 / EU Annex 11 audit trail requirements."
        ),
    ),
    PistoiaIndicator(
        id="PA-R-G1",
        dimension="R",
        level=MaturityLevel.GOLD,
        name="Rich metadata enables assessment of fitness for reuse",
        criterion=(
            "A new user with no prior knowledge of the dataset can determine — from the "
            "metadata alone — whether the dataset is appropriate for their specific "
            "reuse purpose, without contacting the data owner."
        ),
        rda_indicator_ids=["RDA-R1-01M", "RDA-R1.2-01M", "RDA-R1.3-01M"],
        pharma_context=(
            "Include in metadata: assay performance characteristics (Z-factor, signal:noise), "
            "known batch effects or data quality issues, intended and excluded use cases, "
            "data maturity (raw/processed/curated), and recommended analysis approach."
        ),
    ),
    PistoiaIndicator(
        id="PA-R-G2",
        dimension="R",
        level=MaturityLevel.GOLD,
        name="Data complies with domain community standard",
        criterion=(
            "Data is formatted and validated against the community-recognised standard "
            "for the data type. Validation is automated at submission time."
        ),
        rda_indicator_ids=["RDA-R1.3-01D", "RDA-R1.3-02D", "RDA-R1.3-02M"],
        pharma_context=(
            "Bioassay: ISA-Tab; Mass spec: mzML; Genomics: FASTQ + BIDS; Chemistry: SDF/MOL2; "
            "Clinical: CDISC SDTM/ADaM; Imaging: DICOM. "
            "Validation tools: isatools (ISA-Tab), mzML XSD validator, BIDS-validator."
        ),
    ),
    PistoiaIndicator(
        id="PA-R-P1",
        dimension="R",
        level=MaturityLevel.PLATINUM,
        name="Automated FAIR score tracking and improvement loops",
        criterion=(
            "FAIR scores are calculated automatically for all new datasets at ingestion, "
            "tracked over time, and drive continuous improvement through automated alerts "
            "and stewardship workflows when scores fall below threshold."
        ),
        rda_indicator_ids=[
            "RDA-F1-01D", "RDA-F2-01M", "RDA-A1-02M",
            "RDA-I2-01M", "RDA-R1.1-01M", "RDA-R1.3-01M",
        ],
        pharma_context=(
            "Implement a FAIR scoring microservice that integrates with the data catalogue. "
            "Trigger stewardship tickets when metadata is incomplete. "
            "Publish FAIR score dashboards to incentivise data producers. "
            "This is the target state for the agentic FAIR scorer module of this toolkit."
        ),
    ),
]


def get_matrix_by_level(level: MaturityLevel) -> list[PistoiaIndicator]:
    return [i for i in PISTOIA_MATRIX if i.level == level]


def get_matrix_by_dimension(dimension: str) -> list[PistoiaIndicator]:
    return [i for i in PISTOIA_MATRIX if i.dimension.upper() == dimension.upper()]


def describe_level(level: MaturityLevel) -> str:
    return LEVEL_DESCRIPTIONS[level]

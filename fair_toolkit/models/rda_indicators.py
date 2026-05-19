"""
RDA FAIR Maturity Model — all 41 indicators.

Source: RDA FAIR Data Maturity Model Working Group (2020)
        https://doi.org/10.15497/rda00050

Each indicator has:
  - A unique ID (e.g. "RDA-F1-01M")
  - The FAIR principle and sub-principle it belongs to
  - A scope: Metadata (M), Data (D), or Both
  - A priority: Essential, Important, or Useful
  - A human-readable name and assessment question
  - Guidance on how to evaluate compliance
"""

from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────────


class FAIRPrinciple(str, Enum):
    F = "F"  # Findable
    A = "A"  # Accessible
    I = "I"  # Interoperable
    R = "R"  # Reusable


class FAIRSubPrinciple(str, Enum):
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    A1 = "A1"
    A1_1 = "A1.1"
    A1_2 = "A1.2"
    A2 = "A2"
    I1 = "I1"
    I2 = "I2"
    I3 = "I3"
    R1 = "R1"
    R1_1 = "R1.1"
    R1_2 = "R1.2"
    R1_3 = "R1.3"


class IndicatorScope(str, Enum):
    METADATA = "M"   # Applies to metadata
    DATA = "D"       # Applies to data
    BOTH = "MD"      # Applies to both metadata and data


class EvidenceLevel(str, Enum):
    ESSENTIAL = "essential"   # Must be met for minimum FAIR compliance
    IMPORTANT = "important"   # Should be met for meaningful FAIR compliance
    USEFUL = "useful"         # Nice to have; improves overall FAIRness


class ComplianceScore(str, Enum):
    NOT_APPLICABLE        = "not_applicable"         # excluded from score
    NOT_ASSESSED          = "not_assessed"           # excluded from score
    FULLY_IMPLEMENTED     = "fully_implemented"      # 100 %
    IN_IMPLEMENTATION     = "in_implementation"      #  50 %
    UNDER_CONSIDERATION   = "under_consideration"    #  10 %
    NOT_BEING_CONSIDERED  = "not_being_considered"   #   0 %


# Fraction of indicator weight earned per compliance level
SCORE_WEIGHT: dict[ComplianceScore, float] = {
    ComplianceScore.NOT_APPLICABLE:       0.0,
    ComplianceScore.NOT_ASSESSED:         0.0,
    ComplianceScore.FULLY_IMPLEMENTED:    1.0,
    ComplianceScore.IN_IMPLEMENTATION:    0.5,
    ComplianceScore.UNDER_CONSIDERATION:  0.1,
    ComplianceScore.NOT_BEING_CONSIDERED: 0.0,
}

# Priority weights: Essential=3, Important=2, Useful=1
PRIORITY_WEIGHT: dict["EvidenceLevel", int] = {}  # populated after EvidenceLevel is defined


# Populate PRIORITY_WEIGHT now that EvidenceLevel is defined
PRIORITY_WEIGHT.update({
    EvidenceLevel.ESSENTIAL:  3,
    EvidenceLevel.IMPORTANT:  2,
    EvidenceLevel.USEFUL:     1,
})


# ── Model ──────────────────────────────────────────────────────────────────


class RDAIndicator(BaseModel):
    id: str = Field(description="Unique indicator ID, e.g. 'RDA-F1-01M'")
    principle: FAIRPrinciple
    sub_principle: FAIRSubPrinciple
    scope: IndicatorScope
    priority: EvidenceLevel
    name: str = Field(description="Short indicator name")
    question: str = Field(description="The question an assessor answers")
    guidance: str = Field(description="How to evaluate / what to look for")
    description: Optional[str] = Field(default=None, description="Practical description of what this indicator means in context")
    example: Optional[str] = Field(default=None, description="Concrete example of compliance")


# ── All 41 RDA FAIR Maturity Indicators ───────────────────────────────────

RDA_INDICATORS: list[RDAIndicator] = [

    # ── F1: Globally unique and persistent identifiers ────────────────────
    RDAIndicator(
        id="RDA-F1-01M",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata is identified by a persistent identifier",
        question="Is the metadata record assigned a persistent, globally unique identifier (PID)?",
        guidance=(
            "Check whether the metadata record itself (not just the data) has a PID such as "
            "a DOI, ARK, Handle, or IGSN. The PID must resolve to the metadata record. "
            "Verify the PID is registered with a recognised PID authority."
        ),
        description=(
            "Links/pointers between metadata and datasets the metadata don't explicitly describe "
            "indicate the type of relationship they share, e.g., 'higher dose than', 'entry experiment of', etc."
        ),
        example="Display 'Related Data' with other levels aside from described study, etc.",
    ),
    RDAIndicator(
        id="RDA-F1-01D",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Data is identified by a persistent identifier",
        question="Is each data object assigned a persistent, globally unique identifier?",
        guidance=(
            "Verify that the data file or dataset is assigned a PID (DOI, ARK, Handle, IGSN, etc.) "
            "that persists independently of the storage location. "
            "The PID should resolve to the data or a landing page describing access."
        ),
        description=(
            "Links/pointers between metadata indicate the type of relationship they share, "
            "e.g., 'higher dose than', 'entry experiment of', etc.; "
            "a lighter version of a graph Database/Knowledge Graph"
        ),
        example='{"Entry": "https://data.example.org/Study/Entry/STUDY-12345/202305v2", "ProjectStart":"https://data.example.org/Study/ProjectStart/STUDY-12345/202302v1"}',
    ),
    RDAIndicator(
        id="RDA-F1-02M",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata is identified by a globally unique identifier",
        question="Is the metadata identifier globally unique (not just locally unique within a system)?",
        guidance=(
            "The identifier must be unique across all systems globally, not just within the "
            "organisation's own infrastructure. UUIDs assigned by a local LIMS without "
            "a globally registered namespace do NOT qualify."
        ),
        description=(
            "Any use of controlled vocabularies across metadata are explicitly associated with "
            "an ontology service identifier and/or external ontology ID"
        ),
        example="Machine-readable values are replaced with human-readable for download and viewing",
    ),
    RDAIndicator(
        id="RDA-F1-02D",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Data is identified by a globally unique identifier",
        question="Is the data identifier globally unique?",
        guidance=(
            "Same criteria as RDA-F1-02M but applied to the data identifier. "
            "If metadata and data share a single PID (common in repositories like Zenodo), "
            "score both F1-01D and F1-02D as compliant."
        ),
        description=(
            "If possible, study data are directly interoperable and indicate other/previous "
            "associated data from the same compound, modality testing, analyte, etc."
        ),
        example="Column 'See Also' within data or similar, including additional clinical studies examining same gene/mutation",
    ),

    # ── F2: Data described with rich metadata ─────────────────────────────
    RDAIndicator(
        id="RDA-F2-01M",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F2,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Rich metadata describing context, quality, and basic characteristics",
        question=(
            "Does the metadata include descriptive information about the data's context, "
            "quality, condition, and basic characteristics?"
        ),
        guidance=(
            "Metadata should go beyond a simple title and date. Look for: assay type, "
            "experimental conditions, organism/cell line, data quality indicators, "
            "collection methodology, and any processing steps applied. "
            "Richer metadata = more findable by researchers with specific needs."
        ),
        description=(
            "Data lakes and infrastructure systems should be built on standard cloud platforms "
            "using infrastructure-as-code and within the confines of enterprise governance, "
            "identity, and access management requirements"
        ),
        example="Enterprise IT standards and approved cloud infrastructure (data lake, processing platforms, etc.) are used",
    ),

    # ── F3: Metadata explicitly includes the data identifier ─────────────
    RDAIndicator(
        id="RDA-F3-01M",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata includes the identifier for the data it describes",
        question="Does the metadata record explicitly include the PID of the data it describes?",
        guidance=(
            "The link must be in the metadata itself (e.g., a 'relatedIdentifier' field with "
            "relationType='IsDescribedBy'). It is not sufficient for the data and metadata "
            "to share a landing page — the metadata record must explicitly point to the data PID."
        ),
        description=(
            "Any use of controlled vocabularies across data are explicitly associated with "
            "an ontology service identifier and/or external ontology ID"
        ),
        example="Machine-readable values are replaced with human-readable for download and viewing",
    ),

    # ── F4: Metadata registered/indexed in a searchable resource ─────────
    RDAIndicator(
        id="RDA-F4-01M",
        principle=FAIRPrinciple.F,
        sub_principle=FAIRSubPrinciple.F4,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata is harvestable and indexed",
        question="Is the metadata exposed in a way that allows harvesting and indexing by search engines?",
        guidance=(
            "The metadata must be discoverable via standard protocols (OAI-PMH, SPARQL endpoint, "
            "schema.org markup, or DataCite/Crossref APIs). Registration in a domain repository "
            "(e.g., ChEMBL, EBI, Zenodo, Figshare, FAIRsharing) that exposes OAI-PMH satisfies this."
        ),
        description=(
            "Links/pointers between data within datasets indicate the type of relationship the data share, "
            "e.g., 'higher dose than', 'entry experiment of', etc."
        ),
        example="Add key columns in data for rows - Decreases, Increases, Inhibits, etc.",
    ),

    # ── A1: Retrievable by identifier via standardised protocol ──────────
    RDAIndicator(
        id="RDA-A1-01M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata contains access information",
        question="Does the metadata contain information that enables a user to understand how to access the data?",
        guidance=(
            "Metadata should include: access protocol (URL, API endpoint), any authentication "
            "requirements, licence, and contact information if data is not openly accessible. "
            "The access information must be machine-readable."
        ),
        description=(
            "Particularly important for clinical data, allow a user to obtain and view restrictions "
            "on a dataset's specific use requirements"
        ),
        example="Metadata view/download includes a license description and/or link",
    ),
    RDAIndicator(
        id="RDA-A1-02D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Data can be accessed manually (i.e. with human intervention)",
        question="Can the data be accessed manually, i.e. with human intervention?",
        guidance=(
            "Standard terms and language are used to describe provenance for data and metadata."
        ),
        description="Standard terms and language are used to describe provenance for data and metadata",
        example="Use of schema.org terms, FAIRsharing.org (if possible), etc.",
    ),
    RDAIndicator(
        id="RDA-A1-02M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata is accessible via a free and open API",
        question="Can the metadata be retrieved programmatically via a free, open API?",
        guidance=(
            "A REST API, GraphQL endpoint, or SPARQL endpoint that returns metadata without "
            "requiring a subscription or institutional authentication satisfies this. "
            "Check that the API is documented and publicly reachable."
        ),
        description=(
            "Standard formats, terminologies, and value expressions are used in data displays "
            "for machine recognition"
        ),
        example="Use of schema.org terms, FAIRsharing.org (if possible), etc.",
    ),
    RDAIndicator(
        id="RDA-A1-03D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Data identifier resolves to a digital object",
        question="Does the data identifier resolve to a digital object?",
        guidance=(
            "If available, metadata follows a known, accepted recording template "
            "(e.g., a community standard or repository schema)."
        ),
        description=(
            "If available, metadata follows a known, accepted recording template "
            "(e.g., a community standard or repository schema)"
        ),
        example="Use of schema.org terms, FAIRsharing.org (if possible), etc.",
    ),
    RDAIndicator(
        id="RDA-A1-03M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata identifier resolves to a metadata record",
        question="Does the metadata identifier resolve to a metadata record?",
        guidance=(
            "If available, data follows a known, accepted recording template "
            "(e.g., a single source experimental design)."
        ),
        description=(
            "If available, data follows a known, accepted recording template "
            "(e.g., a single source experimental design)"
        ),
        example="Use of schema.org terms, FAIRsharing.org (if possible), etc.",
    ),
    RDAIndicator(
        id="RDA-A1-04D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Data is accessible through standardised protocol",
        question="Can the data be accessed through a standardised protocol?",
        guidance=(
            "A process is included that allows a sufficiently credentialed user to load a new "
            "file/dataset for viewing while assigning appropriate metadata for the backend."
        ),
        description=(
            "A process is included that allows a sufficiently credentialed user to load a new "
            "file/dataset for viewing while assigning appropriate metadata for backend"
        ),
        example='"Upload new data" button',
    ),
    RDAIndicator(
        id="RDA-A1-04M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata accessible through a standardised protocol",
        question="Can the metadata be retrieved via a standardised communication protocol?",
        guidance=(
            "HTTP(S) is the minimum standard. Check that the metadata URL is stable, "
            "responds with appropriate content-type (JSON-LD, Turtle, XML), and returns "
            "a well-formed metadata record."
        ),
        description=(
            "If available, metadata follows a known, accepted template which leverages "
            "already controlled or otherwise machine-readable information"
        ),
        example="Use of schema.org terms, FAIRsharing.org (if possible), etc.",
    ),

    RDAIndicator(
        id="RDA-A1-05D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Data can be accessed automatically (i.e. by a computer program)",
        question="Can the data be accessed automatically, i.e. by a computer program?",
        guidance=(
            "Path of production, use, and contents for data and metadata are included in metadata: "
            "created by, modified by, created on, source, etc."
        ),
        description=(
            "Path of production, use, and contents for data and metadata are included in metadata; "
            "created by, modified by, created on, etc."
        ),
        example='{"Created By":"A Person", "Modified By": "Another Person", "Created On":"01/01/2024 0000","Source":"Internal"}',
    ),

    # ── A1.1: Protocol is open, free, universally implementable ──────────
    RDAIndicator(
        id="RDA-A1.1-01M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1_1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata accessible via open, free protocol",
        question="Is the protocol used to access metadata open, free, and universally implementable?",
        guidance=(
            "HTTP(S), OAI-PMH, SPARQL are open and free. Proprietary protocols (e.g., "
            "vendor-specific LIMS APIs requiring a licence) do not qualify. "
            "The protocol specification must be publicly available."
        ),
        description=(
            "If relevant, metadata contain an identifier for a standardized reuse licence, "
            "not necessarily one that is source-specific - including version information"
        ),
        example='{"License":"MIT Open License"}',
    ),
    RDAIndicator(
        id="RDA-A1.1-01D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1_1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Data accessible via open, free protocol",
        question="Is the protocol used to access data open, free, and universally implementable?",
        guidance=(
            "Same criteria as A1.1-01M applied to data access. HTTP(S), FTP, S3 with public "
            "access qualify. Proprietary streaming protocols or vendor-locked APIs do not."
        ),
        description=(
            "Any attributes, columns, or other key information is linked to external identifiers "
            "where needed, through ontology services, controlled vocabularies, or other reference "
            "systems, rather than relying on a single internal value"
        ),
        example=(
            '"Species" links to an ontology term such as NCIT C45293 '
            "(https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C45293), "
            "and other ontology synonyms, rather than a singular value"
        ),
    ),

    # ── A1.2: Protocol allows authentication/authorisation ────────────────
    RDAIndicator(
        id="RDA-A1.2-01D",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A1_2,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.USEFUL,
        name="Data accessible via access-controlled protocol",
        question=(
            "If access is controlled, does the data access protocol support authentication "
            "and authorisation? Is the access process documented and findable?"
        ),
        guidance=(
            "Look for documented access procedures (Data Access Committee, Material Transfer "
            "Agreement, API key request form). The process itself must be findable from the "
            "metadata record."
        ),
        description=(
            "If relevant, metadata contain a link to a standardized reuse licence, "
            "not necessarily one that is source-specific"
        ),
        example="Link to MIT license",
    ),

    # ── A2: Metadata persists even if data is gone ────────────────────────
    RDAIndicator(
        id="RDA-A2-01M",
        principle=FAIRPrinciple.A,
        sub_principle=FAIRSubPrinciple.A2,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata remains accessible if data is no longer available",
        question="Is the metadata stored in a repository that commits to long-term preservation independent of the data?",
        guidance=(
            "The metadata record must survive even if the underlying data is deleted, "
            "embargoed, or restricted. Repositories that provide this guarantee include "
            "DataCite, Zenodo, and most certified digital repositories (CoreTrustSeal). "
            "A metadata record hosted only in the same system as the data does not qualify."
        ),
        description=(
            "Metadata can be obtained in a JSON/XML (machine-readable) or TSV/CSV (human readable) format"
        ),
        example="Download from UI or obtained from API metadata selection enabled",
    ),

    # ── I1: Formal knowledge representation language ──────────────────────
    RDAIndicator(
        id="RDA-I1-01M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata uses a formal knowledge representation language",
        question="Is the metadata encoded in a standardised, broadly applicable knowledge representation format?",
        guidance=(
            "Formats: RDF (Turtle, JSON-LD, N-Triples), OWL, SKOS. "
            "Tabular formats (CSV, Excel) and unstructured text do NOT qualify. "
            "Structured XML with a published schema is PARTIAL compliance."
        ),
        description=(
            "Any data representation uses templated or otherwise human-readable column names, "
            "value representation, and standard file formats for download (XLSX, TSV, CSV, etc.)"
        ),
        example="Download from UI or obtained from API metadata selection enabled",
    ),
    RDAIndicator(
        id="RDA-I1-01D",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Data uses a standardised representation format",
        question="Is the data encoded in a community-recognised, standardised format?",
        guidance=(
            "Domain-specific standard formats qualify: mzML (proteomics), FASTA/VCF (genomics), "
            "SDF/MOL (chemistry), DICOM (imaging), ISA-Tab (experimental metadata). "
            "Proprietary binary formats (e.g., vendor instrument output) are NOT compliant "
            "unless a public specification exists."
        ),
        description=(
            "Metadata for related studies (e.g. hierarchical study levels such as project -> study -> experiment) "
            "are hierarchically associated within the metadata as are related experimental models, "
            "analytes, reagents, etc."
        ),
        example='{"Entry": "https://data.example.org/Study/Entry/STUDY-12345/202305v2", "ProjectStart":"https://data.example.org/Study/ProjectStart/STUDY-12345/202302v1"}',
    ),
    RDAIndicator(
        id="RDA-I1-02M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata uses machine-understandable knowledge representation",
        question="Is the metadata in a format that machines can parse and understand without human interpretation?",
        guidance=(
            "JSON-LD, RDF/XML, Turtle, and schema.org markup are machine-understandable. "
            "Free-text descriptions and HTML pages without structured markup are NOT. "
            "JSON without a schema/context is PARTIAL."
        ),
        description=(
            "Metadata describing a specific study has direct pointers to not only its own "
            "associated data, but related studies/experiments of the same model, modality, etc."
        ),
        example="Column 'See Also' within data or similar, including additional clinical studies examining same gene/mutation",
    ),
    RDAIndicator(
        id="RDA-I1-02D",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I1,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Data uses machine-understandable representation",
        question="Can the data be parsed and interpreted by machines without ambiguity?",
        guidance=(
            "Machine-understandable means the format has a public specification that software "
            "can implement. Avoid proprietary binary files without public specs. "
            "CSV with a published data dictionary is PARTIAL; CSV with no schema is NOT compliant."
        ),
        description=(
            "Metadata tags and fields which use controlled vocabulary or other standard information "
            "(e.g. study id) will include an alias, synonym in the form of an ontology identifier "
            "or similar machine-interpretable value"
        ),
        example="NCIT, DOID, or other ontology identifiers for values and concepts, 'raw' data column names stored",
    ),

    # ── I2: FAIR vocabularies ─────────────────────────────────────────────
    RDAIndicator(
        id="RDA-I2-01M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I2,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata uses FAIR-compliant vocabularies",
        question=(
            "Do the vocabularies, ontologies, or controlled terminologies used in the metadata "
            "themselves follow FAIR principles (have PIDs, machine-readable formats, open access)?"
        ),
        guidance=(
            "FAIR-compliant vocabularies: OBO Foundry ontologies (OBI, ChEBI, GO, CL, DOID), "
            "Schema.org, Dublin Core, DCAT. Non-FAIR: in-house codebooks without PIDs, "
            "local abbreviation lists with no public documentation."
        ),
        description=(
            "Metadata fields for structured data include information on the experimental model, "
            "procedure(s), reagents, analytes, etc. to enable interoperability. Additionally, "
            "metadata are using documented controlled vocabulary sources where possible "
            "(able to look at the metadata phase)."
        ),
        example="Mouse vs. mus musculus vs. C57/BL6 resolve to the same information",
    ),
    RDAIndicator(
        id="RDA-I2-01D",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I2,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.USEFUL,
        name="Data uses FAIR-compliant vocabularies",
        question="Do controlled terms used within the data files themselves reference FAIR vocabularies?",
        guidance=(
            "Column headers, categorical values, and code lists within data files should "
            "reference ontology terms (e.g., include OBI IDs alongside human-readable labels). "
            "Free-text values with no ontology linkage are NOT compliant."
        ),
        description=(
            "Data fields are described using synonym/alias information for result values, "
            "column names, and other aspects of data representation"
        ),
        example="Where relevant, coded representation (e.g., 1 = Male, 2 = Female, 999 = Unknown) within a JSON/XML/etc. is applied",
    ),

    # ── I3: Qualified references to other (meta)data ──────────────────────
    RDAIndicator(
        id="RDA-I3-01M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata includes qualified references to related resources",
        question=(
            "Does the metadata include links to related datasets, publications, protocols, "
            "or other resources using typed relationships?"
        ),
        guidance=(
            "Links must use typed relationships (not bare URLs). In DataCite: relatedIdentifier with "
            "relationType values (IsCitedBy, IsVersionOf, IsDerivedFrom, IsPartOf). "
            "In schema.org: 'isBasedOn', 'citation'. Bare hyperlinks without relationship type = NOT compliant."
        ),
        description=(
            "Using an enterprise GUID standard, a resolvable GUID is available and assigned to the metadata entity"
        ),
        example="https://metadata.example.org/Study/invitroPD/COMPOUND-001/202402v1",
    ),
    RDAIndicator(
        id="RDA-I3-01D",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.USEFUL,
        name="Data includes qualified references to other data",
        question="Does the data file or dataset include typed links to related data resources?",
        guidance=(
            "Cross-references within the data file should use resolvable identifiers. "
            "E.g., a gene expression dataset referencing compound by ChEMBL ID, "
            "or a protein structure referencing UniProt accession."
        ),
        description=(
            "Indicate whether the data associated with each entity present has a persistent identifier, "
            "enabling provenance tracing, traceback, filtering, and resolution "
            "(e.g., internal identifier linked to a globally unique identifier standard)"
        ),
        example="COMPOUND-001; COMPOUND-002",
    ),
    RDAIndicator(
        id="RDA-I3-02M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.USEFUL,
        name="Metadata includes qualified references to other metadata",
        question="Does the metadata cross-reference other metadata records using typed, resolvable identifiers?",
        guidance=(
            "E.g., the study-level metadata references sub-dataset metadata records, "
            "the dataset metadata references the project metadata, etc., using typed links."
        ),
        description=(
            'A field within the metadata structure includes "Study ID"; "Study"; "Experiment ID"; or similar'
        ),
        example='{"Study ID": "STUDY-001"}',
    ),
    RDAIndicator(
        id="RDA-I3-02D",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.USEFUL,
        name="Data includes links between different types of data",
        question="Are typed links included in the data that connect different data types or modalities?",
        guidance=(
            "Particularly important in multi-omics or multi-assay datasets. "
            "A genomics dataset linking to proteomics data from the same study "
            "using resolvable PIDs with typed relationships."
        ),
        description=(
            "API, FTP, and/or other programmatically accessible resources are available for the data product"
        ),
        example="backend API is active",
    ),
    RDAIndicator(
        id="RDA-I3-03M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata includes qualified references to related resources (broader)",
        question="Does the metadata link to methodologies, software, or instruments used to generate the data?",
        guidance=(
            "Protocol references (protocols.io DOI), software versions (RRID or GitHub release), "
            "instrument models (referenced by their manufacturer ID or RRID) should be included "
            "as typed relatedIdentifier entries."
        ),
        description=(
            "Using an enterprise GUID standard, a resolvable GUID is available and assigned to the data entity"
        ),
        example="https://data.example.org/Study/invitroPD/COMPOUND-001/202402v1",
    ),
    RDAIndicator(
        id="RDA-I3-04M",
        principle=FAIRPrinciple.I,
        sub_principle=FAIRSubPrinciple.I3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.USEFUL,
        name="Metadata includes qualified outward links to related metadata",
        question="Does the metadata explicitly reference metadata standards, schemas, or profiles used?",
        guidance=(
            "The metadata record should declare which schema or application profile it conforms to. "
            "E.g., a DCAT-AP profile URI, a DataCite schema version, or an ISA-Tab profile reference."
        ),
        description=(
            "Indicate whether the metadata associated with each entity present has a persistent identifier, "
            "enabling provenance tracing, traceback, filtering, and resolution "
            "(e.g., internal identifier linked to a globally unique identifier standard)"
        ),
        example="COMPOUND-001; COMPOUND-002",
    ),

    # ── R1: Richly described with accurate, relevant attributes ──────────
    RDAIndicator(
        id="RDA-R1-01M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Plurality of accurate and relevant attributes for reuse",
        question=(
            "Does the metadata provide enough descriptive attributes that a new user could "
            "determine whether the data is appropriate for their specific reuse purpose?"
        ),
        guidance=(
            "Evaluate: domain coverage (methods, conditions, organism, timepoints), "
            "data quality indicators, known limitations, intended use cases. "
            "Compare against community metadata standards (MIAME, MIABI, ISA-Tab) for the domain."
        ),
        description=(
            "Either a GUID or other identifier specific to the data resolves to a view/download "
            "of the data (UI, API ID, etc.)"
        ),
        example=(
            "Go to landing page through - https://data.example.org/Study/invitroPD/COMPOUND-001/202402v1 "
            "or directly download data object through API identifier"
        ),
    ),

    # ── R1.1: Clear and accessible data usage licence ────────────────────
    RDAIndicator(
        id="RDA-R1.1-01M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata includes licence information",
        question="Does the metadata specify under which licence the data can be reused?",
        guidance=(
            "A licence must be explicitly stated. Absence of a licence = 'all rights reserved' "
            "and prevents legal reuse. Acceptable: CC BY 4.0, CC0, MIT, Apache 2.0, ODbL. "
            "Look for a 'license' or 'rights' field in the metadata record."
        ),
        description=(
            "A system within the UI, user-accessible API, or other mechanism allows viewing and/or "
            "download of data - e.g. a data viewing and integration system within the UI, "
            "data download packages, etc."
        ),
        example="Search by analyte, study ID, model system",
    ),
    RDAIndicator(
        id="RDA-R1.1-02M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata refers to a standard reuse licence",
        question="Does the licence referenced in the metadata correspond to a well-known, standard licence?",
        guidance=(
            "Standard licences: Creative Commons family (CC0, CC BY, CC BY-SA, CC BY-NC), "
            "Open Data Commons (ODbL, PDDL), OSI-approved software licences. "
            "Custom or bespoke licences reduce interoperability and reuse. "
            "Check for the canonical licence URL in the metadata."
        ),
        description=(
            "Standard protocols include HTTP/HTTPS (UI-based access) and API/FTP (programmatic access), "
            "allowing authorized users to view study and other associated data"
        ),
        example="An authorized user is able to access data and metadata through UI/API",
    ),
    RDAIndicator(
        id="RDA-R1.1-03M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_1,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata refers to a machine-understandable reuse licence",
        question="Is the licence expressed in a machine-readable format so software can automatically determine reuse rights?",
        guidance=(
            "SPDX licence identifiers (e.g., 'CC-BY-4.0') embedded in metadata enable "
            "automated licence compliance checking. A plain text description of a licence "
            "is NOT machine-understandable. Check for 'spdxExpression' or licence URI fields."
        ),
        description=(
            "Assuming the same restrictions are not imposed on it/them, the descriptive metadata "
            "for any data may still be found after access to data itself is no longer allowed"
        ),
        example="Statement included in license document",
    ),

    # ── R1.2: Detailed provenance ─────────────────────────────────────────
    RDAIndicator(
        id="RDA-R1.2-01M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_2,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Metadata includes cross-domain provenance information",
        question=(
            "Does the metadata include provenance information using a cross-domain "
            "provenance standard (e.g., W3C PROV, PAV, Dublin Core)?"
        ),
        guidance=(
            "Provenance = who created the data, when, from what sources, using what processes. "
            "W3C PROV-O, PAV ontology, and Dublin Core creator/date are cross-domain standards. "
            "A free-text 'notes' field is NOT compliant."
        ),
        description=(
            "Either a GUID or other identifier specific to the metadata resolves to a view/download "
            "of the metadata"
        ),
        example="Go to landing page through - https://metadata.example.org/Study/invitroPD/COMPOUND-001/202402v1",
    ),
    RDAIndicator(
        id="RDA-R1.2-02M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_2,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.USEFUL,
        name="Metadata includes domain-specific provenance information",
        question=(
            "Does the metadata include provenance using domain-specific standards "
            "(e.g., ISA-Tab, MIAME, MIABI, GEO submission format)?"
        ),
        guidance=(
            "Domain-specific provenance goes deeper than cross-domain standards. "
            "For pharma: audit trails in ELN records, 21 CFR Part 11 compliant signatures, "
            "ALCOA+ attributes (Attributable, Legible, Contemporaneous, Original, Accurate)."
        ),
        description=(
            "The metadata contains a field, or set of fields, which include resolvable digital "
            "resources where associated data are housed within the associated data lake"
        ),
        example="Search by analyte, study ID, model system",
    ),

    # ── R1.3: Domain-relevant community standards ─────────────────────────
    RDAIndicator(
        id="RDA-R1.3-01M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.ESSENTIAL,
        name="Metadata complies with a community standard",
        question=(
            "Does the metadata structure comply with a community-recognised metadata standard "
            "for the data type and domain?"
        ),
        guidance=(
            "Check FAIRsharing.org for registered standards for your data type. "
            "Examples: ISA-Tab (experimental biology), MIAME (microarray), MIAPPE (phenotyping), "
            "BIDS (neuroimaging), DataCite Metadata Schema (general research data). "
            "Verify that required fields of the standard are present and populated."
        ),
        description=(
            "Standard protocols include HTTP/HTTPS (UI-based access) and API/FTP (programmatic access), "
            "allowing authorized users to view study and other metadata"
        ),
        example="An authorized user is able to access data and metadata through UI/API",
    ),
    RDAIndicator(
        id="RDA-R1.3-01D",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_3,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.IMPORTANT,
        name="Data complies with a community standard",
        question="Is the data format compliant with a community-recognised standard for the domain?",
        guidance=(
            "Domain data standards: FASTQ/VCF/BAM (genomics), mzML/mzXML (proteomics/metabolomics), "
            "SDF/MOL2/SMILES (chemistry), DICOM (medical imaging), CIF (crystallography). "
            "Check that the file validates against the standard's schema or format specification."
        ),
        description=(
            "Access to any data and metadata is controlled through regulations/policies held by "
            "the data governance function. These can also include enterprise access management "
            "and identity systems, if possible"
        ),
        example="API token(s) assigned, landing pages present behind login/SSO walls",
    ),
    RDAIndicator(
        id="RDA-R1.3-02M",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_3,
        scope=IndicatorScope.METADATA,
        priority=EvidenceLevel.USEFUL,
        name="Metadata expressed in a machine-understandable community standard",
        question=(
            "Is the community standard used for metadata expressed in a machine-understandable format "
            "(RDF, OWL, or published schema with a validator)?"
        ),
        guidance=(
            "Machine-understandable community standards have formal schemas or ontologies. "
            "ISA-Tab has a published schema; BIDS has a JSON schema; DataCite has an XML schema. "
            "Compliance requires that the metadata validates against the schema, not just follows it informally."
        ),
        description=(
            "Any restrictions on use, length of time accessible/restricted, and original source(s) "
            "of data and metadata are recorded and visible to users"
        ),
        example='"License" tab/document present on viewer pages',
    ),
    RDAIndicator(
        id="RDA-R1.3-02D",
        principle=FAIRPrinciple.R,
        sub_principle=FAIRSubPrinciple.R1_3,
        scope=IndicatorScope.DATA,
        priority=EvidenceLevel.USEFUL,
        name="Data expressed in a machine-understandable community standard format",
        question=(
            "Does the data file validate against a machine-checkable specification of the community standard?"
        ),
        guidance=(
            "Use domain validators: mzML validates with XSD schema, VCF validates with bcftools, "
            "BIDS data validates with the BIDS-validator, NMR data validates with NMReDATA validator. "
            "Partial compliance: format follows the standard but has not been formally validated."
        ),
        description=(
            "A system within the UI, user-accessible API, or other mechanism allows viewing and/or "
            "download of metadata - e.g. column headers in a UI, a metadata CSV contained in "
            "a download package, etc."
        ),
        example="Search by analyte, study ID, model system",
    ),
]

# ── Convenience helpers ────────────────────────────────────────────────────


def get_indicators_by_principle(principle: FAIRPrinciple) -> list[RDAIndicator]:
    return [i for i in RDA_INDICATORS if i.principle == principle]


def get_indicators_by_priority(priority: EvidenceLevel) -> list[RDAIndicator]:
    return [i for i in RDA_INDICATORS if i.priority == priority]


def get_indicator(indicator_id: str) -> RDAIndicator | None:
    return next((i for i in RDA_INDICATORS if i.id == indicator_id), None)


INDICATOR_COUNT = len(RDA_INDICATORS)
ESSENTIAL_COUNT = len(get_indicators_by_priority(EvidenceLevel.ESSENTIAL))
IMPORTANT_COUNT = len(get_indicators_by_priority(EvidenceLevel.IMPORTANT))
USEFUL_COUNT = len(get_indicators_by_priority(EvidenceLevel.USEFUL))

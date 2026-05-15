"""
Pistoia Alliance FAIR Maturity Matrix (v1.1, 2025-03-14).

An ORGANISATIONAL maturity model of FAIR implementation for life science
organisations. It is descriptive, not prescriptive.

The matrix is structured as 7 dimensions (rows) × 6 maturity levels (columns).

  7 Dimensions:
    1. FAIR data          — metadata, data, and data products
    2. FAIR leadership    — types and levels of leadership required
    3. FAIR strategy      — vision, plan, and strategic decisions
    4. FAIR roles         — human roles required for FAIR implementation
    5. FAIR processes     — explicit processes to implement FAIR
    6. FAIR knowledge     — factual, conceptual, procedural knowledge needed
    7. FAIR tools         — tools and infrastructures for FAIR

  6 Maturity Levels (L0–L5):
    L0 — "Life is unFAIR"         (Junkyard)
    L1 — "Started the FAIR journey" (Flea market)
    L2 — "Getting FAIR"           (Street Market)
    L3 — "Pretty FAIR"            (Specialized Local Markets)
    L4 — "Really FAIR"            (Hyper Market)
    L5 — "FAIRest of them all"    (Digital Online Store)

Source: https://pistoiaalliance.github.io/FAIRMaturityMatrix/
        Pistoia Alliance FAIR implementation Best Practice Working Group
        Version 1.1, 2025-03-14 | CC BY 4.0
"""

from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MaturityLevel(str, Enum):
    L0 = "L0"   # "Life is unFAIR"
    L1 = "L1"   # "Started the FAIR journey"
    L2 = "L2"   # "Getting FAIR"
    L3 = "L3"   # "Pretty FAIR"
    L4 = "L4"   # "Really FAIR"
    L5 = "L5"   # "FAIRest of them all"


class MatrixDimension(str, Enum):
    DATA        = "FAIR data"
    LEADERSHIP  = "FAIR leadership"
    STRATEGY    = "FAIR strategy"
    ROLES       = "FAIR roles"
    PROCESSES   = "FAIR processes"
    KNOWLEDGE   = "FAIR knowledge"
    TOOLS       = "FAIR tools and infrastructures"


LEVEL_METADATA: dict[MaturityLevel, dict] = {
    MaturityLevel.L0: {
        "nickname": "Life is unFAIR",
        "metaphor": "Junkyard",
        "key_features": "Lack of FAIR awareness, possibly acquiring awareness.",
        "summary": (
            "Data silos and inconsistency impede accessibility and integration. "
            "Minimal leadership involvement. No formal FAIR strategy. "
            "Resistance and cultural barriers may impede FAIR adoption. "
            "Significant deficit in tools and infrastructure for FAIR data management."
        ),
    },
    MaturityLevel.L1: {
        "nickname": "Started the FAIR journey",
        "metaphor": "Flea market",
        "key_features": "FAIR Awareness started; first pilots for implementation may appear.",
        "summary": (
            "Data is siloed and may reside in a shared data platform. "
            "Leadership awareness of FAIR emerges with visionary proposals. "
            "Roles such as curators and semantic experts surface. "
            "Initial plans for tooling and infrastructure emerge. "
            "The 'F' principle (Findability) is the primary focus at this stage."
        ),
    },
    MaturityLevel.L2: {
        "nickname": "Getting FAIR",
        "metaphor": "Street Market",
        "key_features": "FAIR Pilots for implementation are in place.",
        "summary": (
            "Organisation ensures findability through unique identifiers, standardised "
            "metadata, and data registries. Standardised resolution protocols in use. "
            "Initial C-suite engagement. First version of vision/strategy approved. "
            "POC infrastructure in place. Use-cases for machine-findable data begin."
        ),
    },
    MaturityLevel.L3: {
        "nickname": "Pretty FAIR",
        "metaphor": "Specialized Local Markets",
        "key_features": "FAIR Transition to good and best practice.",
        "summary": (
            "FAIR datasets adhering to domain-level models with access controls appear. "
            "Machine interpretation demonstrated locally. Leadership mandates FAIR in "
            "project budgets. Organisation-wide supported plan. COTS tools deployed. "
            "FAIR practices ingrained in workflows in some functions or departments."
        ),
    },
    MaturityLevel.L4: {
        "nickname": "Really FAIR",
        "metaphor": "Hyper Market",
        "key_features": (
            "FAIR operational, best practice known at time of writing. "
            "Internal organisational focus. Emerging cross-organisation focus."
        ),
        "summary": (
            "FAIR principles pervasive across departments. Cross-domain standards, "
            "enterprise-level interoperability, GUPRIs consistently implemented. "
            "Leadership mandates FAIR budgets. Automated tools and registry of "
            "FAIRification tools. Business benefits from FAIR pilots recognised."
        ),
    },
    MaturityLevel.L5: {
        "nickname": "FAIRest of them all",
        "metaphor": "Digital Online Store",
        "key_features": (
            "Largely aspirational: while conceivable, it still needs practical "
            "realisation. Cross-organisation standards and Interoperability."
        ),
        "summary": (
            "FAIR data is the norm; self-describing digital objects are ubiquitous. "
            "Machine actionability and automated AI/semantic solutions act directly on "
            "data without human interpretation. Organisation operates at enterprise AND "
            "ecosystem level. Cross-organisation interoperability is standard. "
            "FAIR is transparent and embedded in daily practice."
        ),
    },
}


class MatrixCell(BaseModel):
    """A single cell in the 7×6 FAIR Maturity Matrix."""
    level: MaturityLevel
    dimension: MatrixDimension
    description: str = Field(description="Description of this cell in the matrix")
    key_features: list[str] = Field(default_factory=list)


# ── The full 7×6 matrix ────────────────────────────────────────────────────

PISTOIA_MATRIX: list[MatrixCell] = [

    # ── FAIR data ──────────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.DATA,
        description=(
            "Data in silos; no consistent metadata; largely unstructured. "
            "No inventory of licences or access policies. "
            "No domain model constraining information."
        ),
        key_features=["No metadata standards", "Data silos", "No identifier policy"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.DATA,
        description=(
            "Some data is cataloged and hosted in a data lake with emerging governance. "
            "Data is generally 'unconformed' (no domain model). "
            "Heterogeneity is a feature: mix of unstructured and pockets of structured data. "
            "Awareness and application of metadata beginning. "
            "Deployment of identifiers starting (not necessarily GUPRIs). "
            "Average technical and expert knowledge required to use data."
        ),
        key_features=["Data lake emerging", "Metadata awareness begins", "Identifiers starting", "Heterogeneous data"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.DATA,
        description=(
            "Data conformed to a local model, cataloged, residing in a data lake. "
            "Data conformed system-by-system; may not map to a domain model. "
            "System-level access controls in place. "
            "Requires average level technical and subject matter knowledge to use."
        ),
        key_features=["Local model conformance", "Data cataloged", "System-level access controls", "PIDs for key datasets"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.DATA,
        description=(
            "FAIR datasets adhering to domain-level models with controlled data access. "
            "Machine interpretation begins to be demonstrated locally (e.g. in a department). "
            "Data conformed to cross-departmental models in some areas."
        ),
        key_features=["Domain-level model conformance", "Controlled access", "Machine interpretation locally", "FAIR datasets emerging"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.DATA,
        description=(
            "FAIR principles pervasive across departments. "
            "Data, metadata, and identifiers conform to cross-domain standards. "
            "Enterprise-level interoperability demonstrated. "
            "Globally Unique, Persistent, Resolvable Identifiers (GUPRIs) consistently implemented."
        ),
        key_features=["Cross-domain standards", "Enterprise interoperability", "GUPRIs", "FAIR pervasive"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.DATA,
        description=(
            "FAIR data is the norm; self-describing (FAIR) digital objects ubiquitous for key data assets. "
            "Machine actionability and automated operations possible. "
            "Machine-enabled AI and semantic solutions act directly on datasets without human interpretation. "
            "Granular data governance and master data management at enterprise and ecosystem level."
        ),
        key_features=["Self-describing data objects", "Machine actionability", "AI-enabled FAIR", "Ecosystem-level interoperability"],
    ),

    # ── FAIR leadership ────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "No FAIR awareness at leadership level. "
            "No engagement with FAIR principles. "
            "Possible resistance to FAIR adoption."
        ),
        key_features=["No FAIR awareness", "No leadership engagement"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "Leadership awareness of FAIR data starts. "
            "Can be top-down or bottom-up leadership approaches. "
            "Some understanding of the potential value of FAIR data; 'thought leaders' emerge. "
            "Visionary proposals for FAIR implementation. "
            "Leadership may fund initial training."
        ),
        key_features=["Leadership awareness begins", "Top-down or bottom-up", "Visionary proposals", "First buy-in"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "Initial C-suite workshops on need and value of FAIR data. "
            "First FAIR projects starting. "
            "Company champions emerge; first teams gather. "
            "Internal workshops creating more awareness. "
            "Leadership-funded initiatives; commitment to enabling key steps. "
            "Memberships to enabling organisations (e.g. for PIDs)."
        ),
        key_features=["C-suite workshops", "First FAIR projects", "Champions emerge", "Leadership funding"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "Leadership sets expectations for FAIR in project budgets. "
            "Establishes organisational metrics related to FAIR. "
            "Refined vision and strategy with organisation-wide supported plan. "
            "Leadership actively manages FAIR implementation."
        ),
        key_features=["FAIR in project budgets", "Organisational FAIR metrics", "Organisation-wide plan", "Active management"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "Leadership mandates include FAIR budgets in all data projects. "
            "Active engagement in the broader FAIR community. "
            "External leadership demonstrated. "
            "Business benefits from FAIR pilots recognised and communicated."
        ),
        key_features=["FAIR budgets mandated", "Community engagement", "External leadership", "ROI demonstrated"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.LEADERSHIP,
        description=(
            "Organisation prioritises FAIR as a strategic AND operational objective. "
            "Operates at enterprise level and ecosystem level. "
            "Acts as a community leader encouraging cross-organisation FAIR adoption. "
            "Maintains critical set of interoperability resources with ecosystem players "
            "(pharma, CROs, solution providers, regulatory bodies, academia)."
        ),
        key_features=["Strategic + operational FAIR", "Community leader", "Ecosystem engagement", "Cross-org standards"],
    ),

    # ── FAIR strategy ──────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.STRATEGY,
        description=(
            "No formal FAIR strategy. "
            "Reactive application if any. "
            "No structured pathway for FAIR implementation."
        ),
        key_features=["No FAIR strategy", "Reactive at best"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.STRATEGY,
        description=(
            "Awareness of FAIR data started; vision and plan begins to emerge. "
            "Different strategies embryonic. "
            "Recognition of FAIR as a strategic asset. "
            "Review of past/current efforts. "
            "Strategic considerations emerge (open vs. closed FAIR resources). "
            "Potential value of pre-competitive collaboration recognised."
        ),
        key_features=["Embryonic FAIR vision", "Strategic recognition", "Exploration phase"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.STRATEGY,
        description=(
            "First version of vision, strategy and plan has approval. "
            "May be at highest company level or more localised. "
            "FAIR emerges as element of a broader data strategy. "
            "Efforts to align FAIR with existing data models. "
            "Realization that technical choices (PIDs, URIs, GUPRIs) have strategic implications."
        ),
        key_features=["First strategy approved", "FAIR in data strategy", "PIDs strategic priority", "Champions appearing"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.STRATEGY,
        description=(
            "Refined vision and strategy exist with organisation-wide supported plan. "
            "FAIR practices becoming ingrained in workflows (at least in some functions). "
            "Integrating formal training into organisational practices. "
            "Continuous improvement processes defined."
        ),
        key_features=["Refined strategy", "Organisation-wide plan", "FAIR in workflows", "Continuous improvement"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.STRATEGY,
        description=(
            "Comprehensive FAIR data strategy encompasses centralised and federated data. "
            "Backed by metrics and integrated into governance processes. "
            "Strategy covers all data domains and functions. "
            "Open-source tools preferred where available."
        ),
        key_features=["Comprehensive strategy", "Metrics-backed", "Governance integrated", "Federated + centralised"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.STRATEGY,
        description=(
            "Comprehensive FAIR strategy at enterprise AND ecosystem level. "
            "Cross-organisation interoperability resources maintained. "
            "Minimal set of cross-organisation standards platforms and tools adopted. "
            "Provenance capture and FAIR principles automated by design."
        ),
        key_features=["Ecosystem strategy", "Cross-org standards", "FAIR by design", "Automated provenance"],
    ),

    # ── FAIR roles ─────────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.ROLES,
        description=(
            "No designated FAIR-related roles. "
            "No formal FAIR knowledge or responsibilities."
        ),
        key_features=["No FAIR roles", "No designated responsibilities"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.ROLES,
        description=(
            "Key emerging roles: curator, semantic expert, data strategist. "
            "Support roles: data coordinator. "
            "External experts (consulting firms) hired to explain and implement FAIR. "
            "Organisation members sent to external workshops (e.g. GO FAIR Foundation). "
            "One individual often covers multiple roles."
        ),
        key_features=["Curator emerges", "Semantic expert emerges", "External experts engaged", "Training starts"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.ROLES,
        description=(
            "Key Role: Data Scientist. "
            "Emerging: data standard expert, data curator, semantic web expert, data strategist, "
            "data stewards, data product owners, community of practice leads. "
            "Designated FAIR-related roles starting to form. "
            "First champions and teams develop Minimal Viable Products (MVPs) and prove value."
        ),
        key_features=["Data Scientist central", "First designated FAIR roles", "MVP teams", "Community managers"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.ROLES,
        description=(
            "Key roles such as data standard experts and curators are established. "
            "Cultural shift towards a data-driven approach begins. "
            "Domain knowledge expertise within each key department. "
            "Broader communities of knowledge and practice forming."
        ),
        key_features=["Data standard experts established", "Domain expertise per dept", "Community of practice", "Data-driven culture"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.ROLES,
        description=(
            "Key roles: data standard experts and Citizen Data Scientists pivotal. "
            "Formalized training programs covering diverse roles. "
            "External leadership demonstrated. "
            "Cross-community collaboration established."
        ),
        key_features=["Citizen Data Scientists", "Formalised training", "External leadership", "Cross-community collaboration"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.ROLES,
        description=(
            "FAIR is transparent for most data citizens; embedded in daily practice. "
            "Organisation promotes organisation-wide understanding with defined roles. "
            "Recognition for FAIR data work. "
            "Complementary organisations in the ecosystem provide interoperability benefits."
        ),
        key_features=["FAIR transparent", "Organisation-wide understanding", "FAIR recognised", "Ecosystem roles"],
    ),

    # ── FAIR processes ─────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.PROCESSES,
        description=(
            "No structured FAIR processes. "
            "Implicit at best. Reactive application of any data processes."
        ),
        key_features=["No FAIR processes", "Ad hoc data management"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.PROCESSES,
        description=(
            "Processes emerging to determine which data to make FAIR retrospectively. "
            "Alignment discussions on metadata centralisation, content management, and reference data. "
            "Culture change processes alongside ad hoc training. "
            "Data domains enter discovery, profiling, and optimisation phases. "
            "Internal and external good practices for FAIR being identified."
        ),
        key_features=["Retrospective FAIRification scoping", "Metadata alignment discussions", "Culture change starts"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.PROCESSES,
        description=(
            "Needs assessments to structure formal training frameworks. "
            "At least one pilot project showcasing FAIR implementation. "
            "Processes include data curation, metadata guidelines, retrospective FAIRification. "
            "FAIR data procurement defined requirements. "
            "Governance processes recognised (master/reference data, RDMs). "
            "Regular retrospectives on pilot projects inform learning."
        ),
        key_features=["Formal training frameworks", "Pilot project", "Metadata guidelines", "FAIR procurement", "Governance recognised"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.PROCESSES,
        description=(
            "FAIR processes ingrained in workflows in at least some functions. "
            "Formal training integrated into organisational practices. "
            "Budget and HR capacity allocated for organisation-wide FAIR delivery. "
            "Processes for FAIR data generation and interaction conceptually defined."
        ),
        key_features=["FAIR in workflows", "Formal training", "Budget allocated", "FAIR generation defined"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.PROCESSES,
        description=(
            "FAIR practices embedded in all workflows. "
            "Continuous improvement with impact measurement. "
            "Adherence to community standards enforced. "
            "Cross-community collaboration and communities of practice established. "
            "Shared learnings and real-world experiences documented."
        ),
        key_features=["FAIR in all workflows", "Continuous improvement", "Standards adherence", "Community of practice"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.PROCESSES,
        description=(
            "FAIR integrated across all data processes, emphasising value throughout lifecycle. "
            "Organisation actively shares learnings in cross-organisation FAIR community of practice. "
            "For most data citizens FAIR is transparent. "
            "Pervasive data-centric culture resists application-centric solutions."
        ),
        key_features=["FAIR in all data processes", "Cross-org community of practice", "Data-centric culture", "FAIR transparent"],
    ),

    # ── FAIR knowledge ─────────────────────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "No FAIR knowledge in the organisation. "
            "Awareness absent or very limited."
        ),
        key_features=["No FAIR knowledge", "No awareness"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "FAIR awareness starts with first workshops by external experts. "
            "People sent to external workshops/training. "
            "Whitepapers and proposals sent to leadership. "
            "Pockets of FAIR knowledge (individuals) but no shared organisational knowledge. "
            "Organisation becomes aware of what it has yet to know. "
            "Individuals connect with external communities of practice (Pistoia Alliance, ELIXIR, academia)."
        ),
        key_features=["External training starts", "Individual knowledge pockets", "External community connection", "Awareness of gaps"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "Designated roles starting to take shape. "
            "FAIR knowledge largely in people but needs formalisation. "
            "Champions and teams can explain and prove value of FAIR. "
            "Internal communities of practice forming around emerging/good practices. "
            "External resources help develop organisation-specific FAIR training. "
            "Knowledge on FAIRification processes begins to be shared. "
            "Vendors and service providers (CROs) play a role in FAIR knowledge ecosystem."
        ),
        key_features=["Roles taking shape", "Internal CoP forming", "Org-specific training", "FAIRification knowledge shared"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "Domain knowledge expertise established within each key department. "
            "Formal training integrated into organisational practices. "
            "Broader communities of knowledge and practice established. "
            "FAIR knowledge becoming systematic rather than individual."
        ),
        key_features=["Domain expertise per dept", "Formal training", "Systematic knowledge", "Broader CoP"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "Formalised training programs covering diverse roles. "
            "Culture of proficiency in FAIR data. "
            "Cross-community collaboration with shared learnings. "
            "Qualitative framework and evaluation metrics for FAIR initiatives."
        ),
        key_features=["Formalised training", "Proficiency culture", "Cross-community learning", "FAIR metrics framework"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.KNOWLEDGE,
        description=(
            "Organisation promotes organisation-wide understanding of FAIR. "
            "Training, defined roles, and recognition for FAIR data work. "
            "Benefits visible for key stakeholders. "
            "Benefits resulting from interoperability and data reuse well documented."
        ),
        key_features=["Organisation-wide FAIR understanding", "FAIR recognition", "Benefits documented", "Reuse value visible"],
    ),

    # ── FAIR tools and infrastructures ────────────────────────────────────
    MatrixCell(
        level=MaturityLevel.L0, dimension=MatrixDimension.TOOLS,
        description=(
            "No FAIR tools or infrastructure. "
            "Unstructured data capture. "
            "No persistent identifier services."
        ),
        key_features=["No FAIR tools", "Unstructured capture", "No PIDs"],
    ),
    MatrixCell(
        level=MaturityLevel.L1, dimension=MatrixDimension.TOOLS,
        description=(
            "Initial plans for tooling and infrastructure for POCs. "
            "Pragmatic progress using existing IT (e.g. Excel templates, drop-down lists). "
            "Centralisation of metadata beginning (CMS, ELN systems, GitHub, Sharepoint, DKAN). "
            "Thinking about and implementing Findability: URI/GUPRI services, published metadata catalogs. "
            "Controlled vocabularies and MDM systems being considered. "
            "At least one policy on unique resource locators."
        ),
        key_features=["POC infrastructure plans", "Existing IT enhanced", "Metadata centralisation starts", "GUPRI/URI policy"],
    ),
    MatrixCell(
        level=MaturityLevel.L2, dimension=MatrixDimension.TOOLS,
        description=(
            "Tools introduced to capture and publish metadata. "
            "Tools to work with controlled vocabularies. "
            "Tools to manage persistent identifiers (PIDs). "
            "FAIR data maturity framework assessments deployed. "
            "POC infrastructure in place; value proven; RFPs for org-wide tooling being scoped. "
            "ELNs play key role in FAIR data principle implementation. "
            "Identifier services; metadata schemas; registries for Findability. "
            "Auth & authorisation services for Accessibility."
        ),
        key_features=["Metadata tools", "Controlled vocabulary tools", "PID management", "FAIR assessment tools", "ELN integration"],
    ),
    MatrixCell(
        level=MaturityLevel.L3, dimension=MatrixDimension.TOOLS,
        description=(
            "COTS (commercial off-the-shelf) or 'standard' tools deployed org-wide where possible. "
            "Budget and HR capacity allocated for organisation-wide FAIR delivery. "
            "Tools for machine-readable metadata. "
            "Domain-specific data standards tools (e.g. CDISC, ISA-Tab converters). "
            "FAIR implementation profile (FIP) tools in use."
        ),
        key_features=["COTS tools deployed", "Machine-readable metadata", "Domain standards tools", "FIP tools"],
    ),
    MatrixCell(
        level=MaturityLevel.L4, dimension=MatrixDimension.TOOLS,
        description=(
            "Automated tools for FAIR data management. "
            "Registry of FAIRification tools available and used. "
            "Defined interaction mechanisms for data access and sharing. "
            "Open-source tools preferred. "
            "Semantic web and knowledge graph technologies deployed."
        ),
        key_features=["Automated FAIR tools", "FAIRification tool registry", "Knowledge graphs", "Open-source preferred"],
    ),
    MatrixCell(
        level=MaturityLevel.L5, dimension=MatrixDimension.TOOLS,
        description=(
            "Minimal set of cross-organisation standards platforms and tools adopted. "
            "Tools designed to automate the creation of FAIR data with provenance capture. "
            "Machine-enabled AI and semantic solutions act on data autonomously. "
            "Cross-ecosystem tooling standards established."
        ),
        key_features=["Cross-org standards platforms", "Automated FAIR creation", "Autonomous AI/semantic tools", "Ecosystem tooling standards"],
    ),
]

# ── Helper functions ──────────────────────────────────────────────────────────

def get_cell(level: MaturityLevel, dimension: MatrixDimension) -> MatrixCell | None:
    """Return the matrix cell for a given level and dimension."""
    for cell in PISTOIA_MATRIX:
        if cell.level == level and cell.dimension == dimension:
            return cell
    return None


def get_level_cells(level: MaturityLevel) -> list[MatrixCell]:
    """Return all 7 dimension cells for a given maturity level."""
    return [cell for cell in PISTOIA_MATRIX if cell.level == level]


def get_dimension_cells(dimension: MatrixDimension) -> list[MatrixCell]:
    """Return all 6 level cells for a given dimension."""
    return [cell for cell in PISTOIA_MATRIX if cell.dimension == dimension]


def describe_level(level: MaturityLevel) -> str:
    """Return a human-readable description of a maturity level."""
    meta = LEVEL_METADATA[level]
    return (
        f"Level {level.value}: \"{meta['nickname']}\" ({meta['metaphor']})\n"
        f"  Key features: {meta['key_features']}\n"
        f"  Summary: {meta['summary']}"
    )

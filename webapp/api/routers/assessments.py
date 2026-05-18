import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from fair_toolkit import ManualFAIRAssessor, ComplianceScore, EvidenceLevel

router = APIRouter()


def _compute_scores(assessment: models.Assessment) -> dict:
    """Run fair_toolkit scoring on stored indicator scores and return enriched dict."""
    assessor = ManualFAIRAssessor(
        dataset_id=assessment.dataset_id,
        dataset_title=assessment.dataset_title,
        assessed_by=assessment.assessed_by or "",
        notes=assessment.notes or "",
    )
    for s in assessment.scores:
        try:
            assessor.score(s.indicator_id, ComplianceScore(s.compliance))
        except (ValueError, KeyError):
            pass

    result = assessor.build_result()
    gaps = result.get_gaps(EvidenceLevel.ESSENTIAL)

    return {
        "id": assessment.id,
        "dataset_id": assessment.dataset_id,
        "dataset_title": assessment.dataset_title,
        "assessed_by": assessment.assessed_by,
        "notes": assessment.notes,
        "created_at": assessment.created_at,
        "updated_at": assessment.updated_at,
        "scores": [
            {
                "indicator_id": s.indicator_id,
                "compliance": s.compliance,
                "evidence": s.evidence,
                "action_notes": s.action_notes,
                "updated_at": s.updated_at,
            }
            for s in assessment.scores
        ],
        "overall_score": result.overall_score,
        "f_score": result.f_score.percentage,
        "a_score": result.a_score.percentage,
        "i_score": result.i_score.percentage,
        "r_score": result.r_score.percentage,
        "essential_gaps": [
            {"indicator_id": g.indicator_id, "indicator_name": g.indicator_name, "principle": g.principle.value}
            for g in gaps
        ],
    }


@router.post("/", status_code=201)
def create_assessment(data: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    a = models.Assessment(
        id=str(uuid.uuid4()),
        **data.model_dump(),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return _compute_scores(a)


@router.get("/")
def list_assessments(db: Session = Depends(get_db)):
    assessments = (
        db.query(models.Assessment)
        .order_by(models.Assessment.created_at.desc())
        .all()
    )
    return [_compute_scores(a) for a in assessments]


@router.get("/{assessment_id}")
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    a = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return _compute_scores(a)


@router.put("/{assessment_id}/scores")
def update_scores(
    assessment_id: str,
    scores: list[schemas.IndicatorScoreIn],
    db: Session = Depends(get_db),
):
    a = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")

    existing_map = {s.indicator_id: s for s in a.scores}

    for s in scores:
        if s.indicator_id in existing_map:
            row = existing_map[s.indicator_id]
            row.compliance = s.compliance
            row.evidence = s.evidence
            row.action_notes = s.action_notes
            row.updated_at = datetime.utcnow()
        else:
            db.add(models.IndicatorScore(
                id=str(uuid.uuid4()),
                assessment_id=assessment_id,
                indicator_id=s.indicator_id,
                compliance=s.compliance,
                evidence=s.evidence,
                action_notes=s.action_notes,
            ))

    a.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(a)
    return _compute_scores(a)


@router.delete("/{assessment_id}", status_code=204)
def delete_assessment(assessment_id: str, db: Session = Depends(get_db)):
    a = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    db.delete(a)
    db.commit()

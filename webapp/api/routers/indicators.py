from fastapi import APIRouter, HTTPException
from fair_toolkit import RDA_INDICATORS, get_indicators_by_principle, FAIRPrinciple

router = APIRouter()


def _serialize(ind):
    return {
        "id": ind.id,
        "principle": ind.principle.value,
        "sub_principle": ind.sub_principle.value,
        "scope": ind.scope.value,
        "priority": ind.priority.value,
        "name": ind.name,
        "question": ind.question,
        "guidance": getattr(ind, "guidance", None),
        "description": getattr(ind, "description", None),
        "example": getattr(ind, "example", None),
    }


@router.get("/")
def list_indicators():
    return [_serialize(ind) for ind in RDA_INDICATORS]


@router.get("/by-principle/{principle}")
def indicators_by_principle(principle: str):
    try:
        p = FAIRPrinciple(principle.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid principle: {principle}. Use F, A, I, or R.")
    return [_serialize(ind) for ind in get_indicators_by_principle(p)]

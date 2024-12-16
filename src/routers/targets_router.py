from fastapi import APIRouter, HTTPException

from src.db import get_session
from fastapi import Depends
from sqlmodel import Session
from src.models import Target
from src.schemas import TargetUpdate

router = APIRouter(prefix="/api/v1")


@router.patch("/targets/{target_id}")
def update_target(target_id: int, target_data: TargetUpdate, db: Session = Depends(get_session)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail=f"Target doesn't exist.")
    if target.complete_state or target.mission.complete_state:
        raise HTTPException(status_code=400, detail=f"You can't update it because of mission/target was completed.")
    target_dumped = target_data.model_dump()
    target.sqlmodel_update(target_dumped)
    db.add(target)
    db.commit()
    db.refresh(target)

    return target

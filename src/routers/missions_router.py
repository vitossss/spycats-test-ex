from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from src.db import get_session
from fastapi import Depends
from sqlmodel import Session, select
from src.models import Mission, Target
from src.schemas import MissionCreate, MissionPublic, MissionUpdate, MissionUpdatePublic

router = APIRouter(prefix="/api/v1")


@router.get("/missions/{mission_id}", response_model=MissionPublic)
def get_mission(mission_id: int, db: Session = Depends(get_session)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission doesn't exist.") 
    
    return mission


@router.get("/missions", response_model=list[MissionPublic])
def get_list_of_missions(db: Session = Depends(get_session)):
    list_of_missions = db.exec(select(Mission).options(selectinload(Mission.targets))).all()
    return list_of_missions


@router.post("/missions", response_model=MissionPublic, status_code=201)
def create_new_mission(mission_data: MissionCreate, db: Session = Depends(get_session)):
    if len(mission_data.targets) > 3 or len(mission_data.targets) == 0:
        raise HTTPException(status_code=400, detail=f"Amount of mission targets must be from 1 to 3.")

    new_mission = Mission(
        complete_state=mission_data.complete_state,
        spycat_id=mission_data.spycat_id,
        targets = [
            Target(
                name=target.name,
                country=target.country,
                notes=target.notes,
                complete_state=target.complete_state
            )
            for target in mission_data.targets
        ]
    )
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)

    return new_mission


@router.patch("/missions/{mission_id}", response_model=MissionUpdatePublic)
def update_mission(mission_id: int, mission_data: MissionUpdate, db: Session = Depends(get_session)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission doesn't exist.")
    mission_dumped = mission_data.model_dump()
    mission.sqlmodel_update(mission_dumped)
    db.add(mission)
    db.commit()
    db.refresh(mission)

    return mission


@router.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_session)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission doesn't exist.")
    if mission.spycat_id:
        raise HTTPException(
            status_code=400,
            detail=f"You can't delete missions with assigned spycat to it."
        )
    db.delete(mission)
    db.commit()

    return {"msg": "Mission successfully deleted."}

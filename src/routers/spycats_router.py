from fastapi import APIRouter, HTTPException
from src.db import get_session
from fastapi import Depends
from sqlmodel import Session, select
from src.models import Spycat
from src.schemas import SpycatPublic, SpycatCreate, SpycatUpdate
import requests


router = APIRouter(prefix="/api/v1")


@router.get("/spycats/{spycat_id}", response_model=SpycatPublic)
def get_spycat(spycat_id: int, db: Session = Depends(get_session)):
    spycat = db.get(Spycat, spycat_id)
    if not spycat:
        raise HTTPException(status_code=404, detail=f"Spycat doesn't exist.") 
    
    return spycat


@router.get("/spycats", response_model=list[SpycatPublic])
def get_list_of_spycats(db: Session = Depends(get_session)):
    list_of_spycats = db.exec(select(Spycat)).all()
    return list_of_spycats


@router.post("/spycats", response_model=SpycatPublic, status_code=201)
def create_new_spycat(spycat_data: SpycatCreate, db: Session = Depends(get_session)):
    list_of_breeds = requests.get("https://api.thecatapi.com/v1/breeds").json()
    for breed in list_of_breeds:
        if spycat_data.breed == breed.get("name"):
            new_spycat = Spycat(**spycat_data.model_dump())
            db.add(new_spycat)
            db.commit()
            db.refresh(new_spycat)

            return new_spycat

    raise HTTPException(status_code=404, detail=f"Spycat with this breed doesn't exist.") 


@router.patch("/spycats/{spycat_id}", response_model=SpycatPublic)
def update_spycat(spycat_id: int, salary: SpycatUpdate, db: Session = Depends(get_session)):
    spycat = db.get(Spycat, spycat_id)
    if not spycat:
        raise HTTPException(status_code=404, detail=f"Spycat doesn't exist.") 
    salary_dumped = salary.model_dump()
    spycat.sqlmodel_update(salary_dumped)
    db.add(spycat)
    db.commit()
    db.refresh(spycat)

    return spycat


@router.delete("/spycats/{spycat_id}")
def delete_spycat(spycat_id: int, db: Session = Depends(get_session)):
    spycat = db.get(Spycat, spycat_id)
    if not spycat:
        raise HTTPException(status_code=404, detail=f"Spycat doesn't exist.") 
    db.delete(spycat)
    db.commit()

    return {"msg": "Spycat successfully deleted."}

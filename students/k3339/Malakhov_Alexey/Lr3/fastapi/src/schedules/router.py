from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.connection import get_session
from schedules.models import Schedule, ScheduleCreate, ScheduleRead, ScheduleUpdate

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/", response_model=List[ScheduleRead])
def schedules_list(session: Session = Depends(get_session)) -> List[ScheduleRead]:
    return session.exec(select(Schedule)).all()


@router.get("/{schedule_id}", response_model=ScheduleRead)
def schedule_get(schedule_id: int, session: Session = Depends(get_session)) -> ScheduleRead:
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule


@router.post("/", status_code=201, response_model=ScheduleRead)
def schedule_create(schedule: ScheduleCreate, session: Session = Depends(get_session)) -> ScheduleRead:
    db_schedule = Schedule.model_validate(schedule)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule


@router.patch("/{schedule_id}", response_model=ScheduleRead)
def schedule_update(
    schedule_id: int, schedule: ScheduleUpdate, session: Session = Depends(get_session)
) -> ScheduleRead:
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule_data = schedule.model_dump(exclude_unset=True)
    for key, value in schedule_data.items():
        setattr(db_schedule, key, value)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule


@router.delete("/{schedule_id}", status_code=204)
def schedule_delete(schedule_id: int, session: Session = Depends(get_session)) -> None:
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    session.delete(db_schedule)
    session.commit()

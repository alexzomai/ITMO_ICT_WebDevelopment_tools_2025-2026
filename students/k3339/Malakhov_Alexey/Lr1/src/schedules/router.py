from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connection import get_session
from schedules.models import Schedule, ScheduleCreate, ScheduleRead, ScheduleUpdate

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/", response_model=List[ScheduleRead])
async def schedules_list(session: AsyncSession = Depends(get_session)) -> List[ScheduleRead]:
    return (await session.exec(select(Schedule))).all()


@router.get("/{schedule_id}", response_model=ScheduleRead)
async def schedule_get(schedule_id: int, session: AsyncSession = Depends(get_session)) -> ScheduleRead:
    db_schedule = await session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule


@router.post("/", status_code=201, response_model=ScheduleRead)
async def schedule_create(schedule: ScheduleCreate, session: AsyncSession = Depends(get_session)) -> ScheduleRead:
    db_schedule = Schedule.model_validate(schedule)
    session.add(db_schedule)
    await session.commit()
    await session.refresh(db_schedule)
    return db_schedule


@router.patch("/{schedule_id}", response_model=ScheduleRead)
async def schedule_update(
    schedule_id: int, schedule: ScheduleUpdate, session: AsyncSession = Depends(get_session)
) -> ScheduleRead:
    db_schedule = await session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in schedule.model_dump(exclude_unset=True).items():
        setattr(db_schedule, key, value)
    session.add(db_schedule)
    await session.commit()
    await session.refresh(db_schedule)
    return db_schedule


@router.delete("/{schedule_id}", status_code=204)
async def schedule_delete(schedule_id: int, session: AsyncSession = Depends(get_session)) -> None:
    db_schedule = await session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    await session.delete(db_schedule)
    await session.commit()

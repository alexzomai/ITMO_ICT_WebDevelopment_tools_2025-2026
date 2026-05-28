from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.connection import get_session
from notifications.models import (
    Notification,
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=List[NotificationRead])
def notifications_list(session: Session = Depends(get_session)) -> List[NotificationRead]:
    return session.exec(select(Notification)).all()


@router.get("/{notification_id}", response_model=NotificationRead)
def notification_get(notification_id: int, session: Session = Depends(get_session)) -> NotificationRead:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


@router.post("/", status_code=201, response_model=NotificationRead)
def notification_create(notification: NotificationCreate, session: Session = Depends(get_session)) -> NotificationRead:
    db_notification = Notification.model_validate(notification)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.patch("/{notification_id}", response_model=NotificationRead)
def notification_update(
    notification_id: int,
    notification: NotificationUpdate,
    session: Session = Depends(get_session),
) -> NotificationRead:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification_data = notification.model_dump(exclude_unset=True)
    for key, value in notification_data.items():
        setattr(db_notification, key, value)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}", status_code=204)
def notification_delete(notification_id: int, session: Session = Depends(get_session)) -> None:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(db_notification)
    session.commit()

from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select

from models import PriorityType, StatusType, Task


def parse_wikipedia(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    for sup in soup.find_all("sup"):
        sup.decompose()

    heading = soup.find("h1", id="firstHeading")
    title = heading.get_text(strip=True) if heading else "Unknown"

    description = ""
    for p in soup.select("#mw-content-text .mw-parser-output > p"):
        text = p.get_text(strip=True)
        if len(text) > 80:
            description = text[:500]
            break

    return title, description or "No description available."


def save_to_db(session: Session, title: str, description: str) -> bool:
    if session.exec(select(Task).where(Task.title == title)).first():
        return False

    session.add(Task(
        title=title,
        description=description,
        status=StatusType.to_do,
        priority=PriorityType.medium,
        deadline=datetime.now(timezone.utc) + timedelta(days=7),
    ))
    session.commit()
    return True


async def save_to_db_async(session: AsyncSession, title: str, description: str) -> bool:
    result = await session.execute(select(Task).where(Task.title == title))
    if result.scalars().first():
        return False

    session.add(Task(
        title=title,
        description=description,
        status=StatusType.to_do,
        priority=PriorityType.medium,
        deadline=datetime.now(timezone.utc) + timedelta(days=7),
    ))
    await session.commit()
    return True

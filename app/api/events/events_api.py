from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.db.session import get_db
from app.api.events.events_schemas import EventCreate, EventRead
from app.data_access.events.events_repository import EventRepository
from app.business_logic.events.events_service import EventService


router = APIRouter()


def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    repository = EventRepository(db)
    return EventService(repository)


@router.get("/events", response_model=list[EventRead])
async def get_events(service: EventService = Depends(get_event_service)):
    return await service.get_events()


@router.get("/events/{event_id}", response_model=EventRead)
async def get_event(
    event_id: int,
    service: EventService = Depends(get_event_service)
):
    try:
        return await service.get_event(event_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/events", response_model=EventRead)
async def create_event(
    event_data: EventCreate,
    service: EventService = Depends(get_event_service)
):
    return await service.create_event(event_data)
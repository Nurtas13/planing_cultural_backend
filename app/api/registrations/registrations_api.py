from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.db.session import get_db
from app.api.registrations.registrations_schemas import RegistrationCreate, RegistrationRead
from app.data_access.registrations.registrations_repository import RegistrationRepository
from app.business_logic.registrations.registrations_service import RegistrationService


router = APIRouter()


def get_registration_service(db: AsyncSession = Depends(get_db)) -> RegistrationService:
    repository = RegistrationRepository(db)
    return RegistrationService(repository)


@router.post("/registrations", response_model=RegistrationRead)
async def create_registration(
    registration_data: RegistrationCreate,
    service: RegistrationService = Depends(get_registration_service)
):
    try:
        return await service.create_registration(registration_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}/registrations", response_model=list[RegistrationRead])
async def get_user_registrations(
    user_id: int,
    service: RegistrationService = Depends(get_registration_service)
):
    return await service.get_user_registrations(user_id)


@router.get("/registrations", response_model=list[RegistrationRead])
async def get_all_registrations(
    service: RegistrationService = Depends(get_registration_service)
):
    return await service.get_all_registrations()


@router.delete("/registrations/{registration_id}")
async def delete_registration(
    registration_id: int,
    service: RegistrationService = Depends(get_registration_service)
):
    try:
        await service.delete_registration(registration_id)
        return {"message": "Registration deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Users"])

@router.get("/")
def get_users():
    return {"users": []}
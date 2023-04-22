from fastapi import APIRouter
from src import schema
from src import methods


router = APIRouter()


@router.post("/health")
async def health(request: schema.Health):
    response = await methods.health(request)
    return response



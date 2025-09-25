from fastapi import APIRouter
from app.schema.models import ModelsResponse
from app.core.openai_service import get_openai_service

router = APIRouter()

@router.get("/models")
def get_models() -> ModelsResponse:
    service = get_openai_service()
    models = service.get_models()
    return ModelsResponse(data=models)


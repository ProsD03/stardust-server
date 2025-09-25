from functools import lru_cache
from typing import List

from app.schema.models import ModelObject
from app.settings.config import get_config, Config
from app.settings.models import get_models


class OpenAIService:
    def __init__(self):
        self.models = get_models()
        self.config = get_config()

    def get_models(self) -> List[ModelObject]:
        model_list = []
        for model in self.models:
            model_object = ModelObject(id=model.name, created=model.created_at.timestamp())
            model_list.append(model_object)
        return model_list

@lru_cache()
def get_openai_service() -> OpenAIService:
    return OpenAIService()

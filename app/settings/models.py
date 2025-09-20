import os
from functools import lru_cache

import yaml
from pydantic import BaseModel


class Model(BaseModel):
    name: str
    prompt: str

class Models(BaseModel):
    models: list[Model]

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        config_dict = yaml.safe_load(open(path))
        super().__init__(**config_dict)

@lru_cache
def get_models():
    return Models(os.environ.get("STARDUST_MODELS_PATH"))

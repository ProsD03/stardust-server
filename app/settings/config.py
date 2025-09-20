import os
from functools import lru_cache
from ipaddress import IPv4Network, IPv6Network

import yaml
from pydantic import BaseModel, SecretStr

class NetworkSettings(BaseModel):
    host: IPv4Network | IPv6Network | str
    port: int

class LLMSettings(BaseModel):
    model: str
    api_key: SecretStr


class Config(BaseModel):
    network: NetworkSettings
    llm: LLMSettings
    embeddings: LLMSettings

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        config_dict = yaml.safe_load(open(path))
        super().__init__(**config_dict)

@lru_cache
def get_config():
    return Config(os.environ.get("STARDUST_CONFIG_PATH"))


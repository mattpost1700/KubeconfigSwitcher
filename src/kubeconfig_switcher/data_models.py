from pydantic import BaseModel


class KubeConfig(BaseModel):
    name: str
    file_contents: str

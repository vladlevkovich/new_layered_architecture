from typing import Optional

from pydantic import BaseModel


class MenuResponse(BaseModel):
    id: int
    name: str
    description: str
    photo: Optional[str]
    is_available: bool

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConfigurationItemBase(BaseModel):
    name: str
    type: str
    status: Optional[str] = "active"
    attributes: Optional[dict] = {}

class ConfigurationItemCreate(ConfigurationItemBase):
    pass

class ConfigurationItem(ConfigurationItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

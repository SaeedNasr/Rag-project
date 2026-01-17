from pydantic import BaseModel , Field , field_validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: str = Field(default=None)
    asset_pused_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    asset_project_id: ObjectId 
    #asset_config: dict = Field(default=None)


    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

    @classmethod
    def get_indexes(cls):
        return [{"key": [("asset_project_id", 1),], "unique": False, "name": "asset_project_id_index"},
                {"key": [("asset_project_id", 1), ("asset_name", 1)], "unique": False, "name": "asset_project_id_name_index"}]
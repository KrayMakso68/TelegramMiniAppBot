from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.camelize_string import camelize


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=lambda s: camelize(s),
                              populate_by_name=True
                              )


class ModelBaseInfo(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

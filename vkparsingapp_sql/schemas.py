from typing import Optional

from pydantic import BaseModel, validator, HttpUrl


class ItemBase(BaseModel):
    link: HttpUrl
    text: Optional[str] = None

    class Config:
        orm_mode = True

    @validator('text', pre=True, always=True)
    def text_validator(cls, v):
        assert len(v) > 0, "Text field can't be empty"
        return v

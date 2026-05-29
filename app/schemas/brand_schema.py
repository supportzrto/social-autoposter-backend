from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str


class BrandResponse(BrandCreate):
    id: int

    class Config:
        from_attributes = True
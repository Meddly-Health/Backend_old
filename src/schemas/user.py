import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserUpdateModel(BaseModel):
    first_name: str | None
    last_name: str | None
    height: float | None
    weight: float | None
    sex: str | None
    birth: datetime.date | None


class UserModel(BaseModel):
    # Atributos obligatorios
    user_id: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime
    diseases: list[str]
    supervisors: list[str]
    supervised: list[str]

    # Atributos opcionales
    first_name: str | None
    last_name: str | None
    height: float | None
    weight: float | None
    sex: str | None
    birth: datetime.date | None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "7TKUuX29JFhbT6t9mnVARy70tXS2",
                "email": "ignacio.pieve@gmail.com",
                "created_at": "2022-04-12T03:31:19.122000",
                "updated_at": "2022-04-12T03:31:19.122000",
                "diseases": ["diabetes", "hipertension"],
                "supervisors": ["7TKUuX29JFhbT6t9mnVARy70tXS3", "7TKUuX29JFhbT6t9mnVARy70tXS4"],
                "supervised": ["7TKUuX29JFhbT6t9mnVARy70tXS5"],

                "first_name": "Ignacio",
                "last_name": "Pieve Roiger",
                "height": 1.70,
                "weight": 67.0,
                "sex": "M",
                "birth": "2000-10-02",
            }
        }

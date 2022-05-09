import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class SupervisorModel(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None

    class Config:
        schema_extra = {
            "example": {
                "email": "example@test.com",
                "first_name": "John",
                "last_name": "Doe",
            }
        }


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
    supervisors: list[SupervisorModel]
    supervised: list[SupervisorModel]

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
                "supervisors": [
                    {
                        "email": "example@test.com",
                        "first_name": "John",
                        "last_name": "Doe",
                    },
                    {
                        "email": "example@test.com",
                        "first_name": "John",
                        "last_name": "Doe",
                    },
                ],
                "supervised": [
                    {
                        "email": "example@test.com",
                        "first_name": "John",
                        "last_name": "Doe",
                    },
                ],
                "first_name": "Ignacio",
                "last_name": "Pieve Roiger",
                "height": 1.70,
                "weight": 67.0,
                "sex": "M",
                "birth": "2000-10-02",
            }
        }

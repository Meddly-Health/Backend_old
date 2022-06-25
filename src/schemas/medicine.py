import datetime
from typing import Literal
from pydantic import BaseModel

"""         ----- Consumption Rules -----         """


class ConsumptionRule(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None


class NeedIt(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["need_it"]


class EveryDay(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["every_day"]
    hours: list[datetime.time]


class EveryXDay(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["every_x_day"]
    number: int


class SpecificDays(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["specific_days"]
    days: list[
        Literal[
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ]
    ]


"""         ----- Medicine -----         """


class Method(BaseModel):
    name: str


class MedicineDosis(Method):
    value: float
    unit: str


class MedicineApplication(Method):
    description: str


class Medicine(BaseModel):
    name: str
    icon: str
    method: Method


"""         ----- Treatment -----         """


class TreatmentIndication(BaseModel):
    consumption_rule: NeedIt | EveryDay | EveryXDay | SpecificDays

    instructions: str | None


class TreatmentModel(BaseModel):
    medicine: Medicine
    treatment_indication: TreatmentIndication

    stock: int | None
    stock_warning: int | None

    class Config:
        schema_extra = {
            "example": {
                "medicine": {
                    "name": "Paracetamol",
                    "icon": "https://www.google.com/",
                    "method": {
                        "name": "Pastilla",
                        "value": 10,
                        "unit": "mg",
                    },
                },
                "treatment_indication": {
                    "instructions": "Tomarlo cada 8 horas",
                    "consumption_rule": {
                        "name": "specific_days",
                        "start": "2022-01-01T00:00:00",
                        "end": "2023-01-01T00:00:00",
                        "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                    },
                },
                "stock": 10,
                "stock_warning": 5,
            }
        }


"""         ----- New Consumption -----         """


class NewConsumption(BaseModel):
    consumption_date: datetime.datetime

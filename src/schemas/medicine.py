import datetime
from typing import Literal

from pydantic import BaseModel

"""         ----- Consumption Rules -----         """


class ConsumptionRule(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None
    name: str


class NeedIt(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["need_it"]


class EveryDay(ConsumptionRule):
    # TODO: Explicar que significa esto @leilaspini
    name: Literal["every_day"]
    hours: list[datetime.time]


class EveryXDay(ConsumptionRule):
    """
    Esta regla de consumos se aplica cada x días, por ejemplo:
        Si el medicamento se debe aplicar cada 2 días (number = 2), a partir del Lunes 1 de Junio a las 17.30,
        las próximas fechas válidas para aplicar el medicamento son:
            - Miércoles 3 de Junio a las 17.30
            - Viernes 5 de Junio a las 17.30
            - Domingo 7 de Junio a las 17.30
            - etc...
    """

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
                        "days": [
                            "monday",
                            "tuesday",
                            "wednesday",
                            "thursday",
                            "friday",
                        ],
                    },
                },
                "stock": 10,
                "stock_warning": 5,
            }
        }


"""         ----- New Consumption -----         """


class NewConsumption(BaseModel):
    consumption_date: datetime.datetime

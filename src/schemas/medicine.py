import datetime
from typing import Literal

from pydantic import BaseModel

"""         ----- Consumption Rules -----         """


class ConsumptionRule(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None
    name: str


class NeedIt(ConsumptionRule):
    """
    Esta regla se aplica cuando el usuario indica que necesita consumir el medicamento
    """

    name: Literal["need_it"]


class EveryDay(ConsumptionRule):
    """
    Esta regla de consumo se aplica todos los días, por ejemplo:
        Si el medicamento se debe aplicar todos los días a las 11.00 y a las 23.00 (hours = [11.00, 23.00]), a partir del Lunes 1 de Junio,
        las próximas fechas válidas para aplicar el medicamento son:
            - Martes 2 de Junio a las 11.00 y luego las 23.00
            - Miércoles 3 de Junio a las 11.00 y luego las 23.00
            - Jueves 4 de Junio a las 11.00 y luego las 23.00
            - Viernes 5 de Junio a las 11.00 y luego las 23.00
            - etc...
    """

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
    """
    Esta regla de consumo se aplica en días específicos, por ejemplo:
        Si el medicamento se debe aplicar los días Martes, Jueves y Sábado (days = ["tuesday", "thursday", "saturday"]), a partir del Martes 2 de Junio a las 17.30,
        las próximas fechas válidas para aplicar el medicamento son:
            - Jueves 4 de Junio a las 17.30
            - Sábado 6 de Junio a las 17.30
            - Martes 9 de Junio a las 17.30
            - etc...
    """

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


class TreatmentUpdateModel(BaseModel):
    medicine: Medicine
    treatment_indication: TreatmentIndication

    stock: int | None
    stock_warning: int | None


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

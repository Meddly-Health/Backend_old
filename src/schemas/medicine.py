import datetime

from typing import Literal

from pydantic import BaseModel, EmailStr, Field

"""         ----- Consumption Rules -----         """


class ConsumptionRule(BaseModel):
    # De este modelo heredan los otros modelos
    pass


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


class Medicine(BaseModel):
    name: str
    # format
    # dosis
    icon: str

    # TODO: Me voy a dormir.
    # TODO: Continuar Medicina y todo lo que hereda de medicina.


"""         ----- Treatment -----         """


class TreatmentIndication(BaseModel):
    start: datetime.datetime

    instructions: str | None
    end: datetime.datetime | None
    consumption_rule: ConsumptionRule


class Treatment(BaseModel):
    name: str
    medicine: Medicine
    treatment_indication: TreatmentIndication

    stock: int | None
    stock_warning: int | None

    class Config:
        schema_extra = {
            # TODO: Example
        }

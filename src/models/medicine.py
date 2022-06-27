from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
import datetime
from typing import Literal

from fastapi import HTTPException
from starlette import status

from schemas.medicine import NewConsumption
from schemas.medicine import NeedIt as NeedItSchema
from schemas.medicine import EveryDay as EveryDaySchema
from schemas.medicine import EveryXDay as EveryXDaySchema
from schemas.medicine import SpecificDays as SpecificDaysSchema


class ConsumptionRule:
    def __init__(self, start: datetime.datetime, end: datetime.datetime = None):
        self.start = start.replace(tzinfo=None)
        self.end = end.replace(tzinfo=None) if end is not None else None

    def validate(self, consumption: NewConsumption):
        if consumption.consumption_date < self.start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consumption date is before the start of the treatment",
            )
        if self.end is not None:
            if consumption.consumption_date > self.end:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The treatment has expired",
                )

    @staticmethod
    def get_consumption_rule(consumption_rule):
        if consumption_rule["name"] == "need_it":
            consumption_rule = NeedItSchema(**consumption_rule)
            return NeedIt(consumption_rule.start, consumption_rule.end)
        elif consumption_rule["name"] == "every_day":
            consumption_rule = EveryDaySchema(**consumption_rule)
            return EveryDay(
                consumption_rule.start, consumption_rule.hours, consumption_rule.end
            )
        elif consumption_rule["name"] == "every_x_day":
            consumption_rule = EveryXDaySchema(**consumption_rule)
            return EveryXDays(
                consumption_rule.start, consumption_rule.number, consumption_rule.end
            )
        elif consumption_rule["name"] == "specific_days":
            consumption_rule = SpecificDaysSchema(**consumption_rule)
            return SpecificDays(
                consumption_rule.start, consumption_rule.days, consumption_rule.end
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown consumption rule",
            )


class NeedIt(ConsumptionRule):
    def __init__(self, start: datetime.datetime, end: datetime.datetime = None):
        super().__init__(start, end)

    def validate(self, consumption: NewConsumption):
        super().validate(consumption)
        return True


class EveryDay(ConsumptionRule):
    def __init__(
        self,
        start: datetime.datetime,
        hours: list[datetime.time],
        end: datetime.datetime = None,
    ):
        super().__init__(start, end)
        self.hours = hours

    def validate(self, consumption: NewConsumption):
        super().validate(consumption)
        # TODO: Implementar @leilaspini
        return True


class EveryXDays(ConsumptionRule):
    def __init__(
        self, start: datetime.datetime, number: int, end: datetime.datetime = None
    ):
        super().__init__(start, end)
        self.number = number

    def validate(self, consumption: NewConsumption):
        super().validate(consumption)
        correct_day = (
            relativedelta(self.start, consumption.consumption_date).days % self.number
        ) == 0
        if not correct_day:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consumption date is not on the correct day",
            )
        correct_hour = consumption.consumption_date.hour == self.start.hour
        correct_minute = consumption.consumption_date.minute == self.start.minute
        correct_time = correct_hour and correct_minute
        if not correct_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consumption date is not on the correct time",
            )
        return True


class SpecificDays(ConsumptionRule):
    def __init__(
        self,
        start: datetime.datetime,
        days: list[
            Literal[
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        ],
        end: datetime.datetime = None,
    ):
        super().__init__(start, end)
        self.days = days

    def validate(self, consumption: NewConsumption):
        super().validate(consumption)
        # TODO: Implementar @leilaspini
        return True


class Treatment:
    def __init__(self):
        self.treatment_id = None
        self.user = None
        self.db = None
        self.treatment = None
        self.consumption_rule = None

    async def load(self, db, user, treatment_id: str):
        self.user = user
        self.db = db
        self.treatment_id = treatment_id
        self.treatment = await self.validate()
        self.consumption_rule: ConsumptionRule = await self.get_consumption_rule()

    async def validate(self):
        response = await self.db["user"].find_one(
            {
                "_id": self.user["user_id"],
                f"treatments.{self.treatment_id}": {"$exists": True},
            },
            {f"treatments.{self.treatment_id}": 1},
        )

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Treatment not found"
            )
        return response["treatments"][self.treatment_id]

    async def get_consumption_rule(self):
        return ConsumptionRule.get_consumption_rule(
            self.treatment["treatment_indication"]["consumption_rule"]
        )

    async def add_consumption(self, consumption: NewConsumption):
        consumption.consumption_date = consumption.consumption_date.replace(tzinfo=None)
        if self.consumption_rule.validate(consumption):
            await self.db["user"].update_one(
                {"_id": self.user["user_id"]},
                {
                    "$set": {
                        f"treatments.{self.treatment_id}.history.{str(consumption.consumption_date.date())}.{f'{consumption.consumption_date.hour}:{consumption.consumption_date.minute}'}": True
                    }
                },
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consumption time or date is not valid",
            )

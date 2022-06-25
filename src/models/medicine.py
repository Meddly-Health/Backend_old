import datetime
from typing import Literal

from fastapi import HTTPException
from starlette import status

from schemas.medicine import NewConsumption


class ConsumptionRule:
    def __init__(self, start: datetime.datetime, end: datetime.datetime = None):
        self.start = start
        self.end = end

    def validate(self, consumption: NewConsumption):
        pass

    @staticmethod
    def get_consumption_rule(consumption_rule):
        if consumption_rule["name"] == "need_it":
            return NeedIt(consumption_rule["start"], consumption_rule["end"])
        elif consumption_rule["name"] == "every_day":
            return EveryDay(
                consumption_rule["start"],
                consumption_rule["end"],
                consumption_rule["hours"],
            )
        elif consumption_rule["name"] == "every_x_day":
            return EveryXDays(
                consumption_rule["start"],
                consumption_rule["end"],
                consumption_rule["number"],
            )
        elif consumption_rule["name"] == "specific_days":
            return SpecificDays(
                consumption_rule["start"],
                consumption_rule["end"],
                consumption_rule["days"],
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
        # TODO: Implementar @leilaspini
        return True


class EveryXDays(ConsumptionRule):
    def __init__(
        self, start: datetime.datetime, number: int, end: datetime.datetime = None
    ):
        super().__init__(start, end)
        self.number = number

    def validate(self, consumption: NewConsumption):
        # TODO: Implementar @leilaspini
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
                detail="Consumption time is not valid",
            )

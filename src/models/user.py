import datetime
import random
import string

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from medicine import *
from starlette import status


class User:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    async def assert_user(self):
        """
        Esta función se asegura de que el usuario exista en la base de datos, y, en caso de no hacerlo,
        lo crea estableciendo los parametros iniciales
        """
        user = await self.db["user"].find_one({"_id": self.user["user_id"]})
        if not user:
            user = {
                "_id": self.user["user_id"],
                "email": self.user["email"],
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
                "diseases": [],
                "supervisors": [],
                "supervised": [],
                "invitation": await self.generate_code(),
            }
            await self.db["user"].insert_one(user)

    async def get(self):
        pipeline = [
            {"$match": {"_id": self.user["user_id"]}},
            {
                "$lookup": {
                    "from": "user",
                    "localField": "supervised",
                    "foreignField": "_id",
                    "as": "supervised",
                    "pipeline": [
                        {
                            "$project": {
                                "avatar": 1,
                                "email": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "_id": 1,
                            }
                        },
                    ],
                }
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "supervisors",
                    "foreignField": "_id",
                    "as": "supervisors",
                    "pipeline": [
                        {
                            "$project": {
                                "avatar": 1,
                                "email": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "_id": 1,
                            }
                        },
                    ],
                }
            },
        ]
        user = (await self.db["user"].aggregate(pipeline).to_list(length=1))[0]
        return user

    async def update(self, user_data):
        user_data = jsonable_encoder(user_data)
        user_data["updated_at"] = datetime.datetime.now()

        await self.db["user"].update_one(
            {"_id": self.user["user_id"]}, {"$set": user_data}
        )
        user = await self.get()
        return user

    async def delete(self):
        await self.db["user"].delete_one({"_id": self.user["user_id"]})
        return {"status": "ok"}

    async def delete_supervised(self, supervised_id):
        supervisor = await self.db["user"].find_one({"_id": self.user["user_id"]})
        supervised = await self.db["user"].find_one({"_id": supervised_id})

        if (supervisor is None or supervised is None) or (
            supervised["_id"] not in supervisor["supervised"]
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found (maybe this user is not being supervised by you)",
            )

        supervised["supervisors"].remove(self.user["user_id"])
        supervisor["supervised"].remove(supervised_id)

        await self.db["user"].update_one(
            {"_id": self.user["user_id"]}, {"$set": supervisor}
        )
        await self.db["user"].update_one({"_id": supervised_id}, {"$set": supervised})

        return {"status": "ok"}

    async def delete_supevisor(self, supervisor_id):
        supervisor = await self.db["user"].find_one({"_id": supervisor_id})
        supervised = await self.db["user"].find_one({"_id": self.user["user_id"]})

        if (supervisor is None or supervised is None) or (
            supervised["_id"] not in supervisor["supervised"]
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found (maybe you are not being supervised by this user)",
            )

        supervised["supervisors"].remove(supervisor_id)
        supervisor["supervised"].remove(self.user["user_id"])

        await self.db["user"].update_one({"_id": supervisor_id}, {"$set": supervisor})
        await self.db["user"].update_one(
            {"_id": self.user["user_id"]}, {"$set": supervised}
        )

        return {"status": "ok"}

    async def accept_invitation(self, code):
        supervisor = await self.db["user"].find_one({"invitation": code})
        supervised = await self.db["user"].find_one({"_id": self.user["user_id"]})

        if supervisor:
            if supervisor["_id"] == supervised["_id"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You can't invite yourself",
                )

            if supervised["_id"] in supervisor["supervised"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You are already being supervised by this user",
                )

            supervisor["invitation"] = await self.generate_code()
            supervisor["supervised"].append(supervised["_id"])
            supervised["supervisors"].append(supervisor["_id"])

            await self.db["user"].update_one(
                {"_id": supervised["_id"]}, {"$set": supervised}
            )
            await self.db["user"].update_one(
                {"_id": supervisor["_id"]}, {"$set": supervisor}
            )

            return {"status": "ok"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    async def generate_code(self):
        """
        Generates a 10-character code and checks that it does not exist in the database
        """

        async def generate():
            generated_code = []
            for k in [3, 4, 3]:
                generated_code.append(
                    "".join(random.choices(string.ascii_uppercase, k=k))
                )
            generated_code = "-".join(generated_code).upper()
            return generated_code

        async def is_repeated(code_to_check):
            code_is_repeated = await self.db["user"].find_one(
                {"invitation": code_to_check}
            )
            return code_is_repeated is not None

        code = await generate()
        while await is_repeated(code):
            code = await generate()

        return code

    async def add_treatment(self, treatment: Treatment):
        pass

    async def mark_consumption(self, treatment_id: str, consumption: Consumption):
        pass

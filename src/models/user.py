import datetime

from fastapi.encoders import jsonable_encoder


class User:
    @staticmethod
    async def get(db, user):
        pipeline = [
            {"$match": {"_id": user["user_id"]}},
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
        print("PENE")
        user = (await db["user"].aggregate(pipeline).to_list(length=1))[0]
        print("PENE2")
        print(user)
        return user

    @classmethod
    async def update(cls, db, user, user_data):
        user_data = jsonable_encoder(user_data)
        user_data["updated_at"] = datetime.datetime.now()

        await db["user"].update_one({"_id": user["user_id"]}, {"$set": user_data})
        return cls.get(db, user)

    @staticmethod
    async def delete(db, user):
        # TODO: Eliminar todos los datos del usuario (y sus relaciones)

        await db["user"].delete_one({"_id": user["user_id"]})
        return {"status": "ok"}

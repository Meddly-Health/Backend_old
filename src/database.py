import datetime

from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import GEO2D

from config import db_name, db_string


class Database:
    db_client: AsyncIOMotorClient = None
    testing = False

    @staticmethod
    async def get_db():
        if Database.testing:
            return Database.db_client[f"{db_name}_test"]
        return Database.db_client[db_name]

    @staticmethod
    async def connect_db():
        """Create database connection."""
        Database.db_client = AsyncIOMotorClient(db_string)

        if Database.testing:
            await Database.db_client.drop_database(f"{db_name}_test")
            user = {
                "user_id": "test_id",
                "email": "example@test.com",
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
                "diseases": [],
                "supervisors": [],
                "supervised": [],
            }
            await Database.db_client[f"{db_name}_test"]["user"].insert_one(user)

    @staticmethod
    async def close_db():
        """Close database connection."""
        Database.db_client.close()

from motor.motor_asyncio import AsyncIOMotorClient

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

        await Database.generate_indexes()

    @staticmethod
    async def close_db():
        """Close database connection."""
        Database.db_client.close()

    @staticmethod
    async def generate_indexes():
        # TODO: Hay que definir los indices
        pass

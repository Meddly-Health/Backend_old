from motor.motor_asyncio import AsyncIOMotorClient
if __name__ == "__main__":
    try:
        import set_environ
    except ModuleNotFoundError:
        pass
from config import db_name, db_string, env_name


class Database:
    db_client: AsyncIOMotorClient = None
    testing = False

    @classmethod
    async def get_db(cls):
        database_name = await cls.get_db_name()
        return cls.db_client[database_name]

    @classmethod
    async def connect_db(cls):
        """Create database connection."""
        cls.db_client = AsyncIOMotorClient(db_string)

        if cls.testing:
            database_name = await cls.get_db_name()
            await cls.db_client.drop_database(database_name)

        await cls.generate_indexes()

    @classmethod
    async def get_db_name(cls):
        if cls.testing and env_name == "dev":
            database_name = f"{db_name}_dev_test"
        elif cls.testing:
            database_name = f"{db_name}_test"
        elif env_name != "production":
            database_name = f"{db_name}_{env_name}"
        else:
            database_name = db_name
        return database_name

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        cls.db_client.close()

    @staticmethod
    async def generate_indexes():
        # TODO: Hay que definir los indices
        pass


if __name__ == "__main__":
    import asyncio

    async def main():
        await Database.connect_db()
        db = await Database.get_db()

        # ZONA DE PRUEBAS

        # ZONA DE PRUEBAS

    asyncio.run(main())

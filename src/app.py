from fastapi import FastAPI

import config
from database import Database
from routers import test, user

app = FastAPI(**config.metadata)

app.include_router(user.router)
app.include_router(test.router)

app.add_event_handler("startup", Database.connect_db)
app.add_event_handler("shutdown", Database.close_db)

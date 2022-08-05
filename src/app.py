try:
    import set_environ
except ModuleNotFoundError:
    print('set_environ.py not found, using system environment variables')

from fastapi import FastAPI

import config
from database import Database
from routers import medicine, supervisors, test, user

app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisors.router)
app.include_router(medicine.router)
app.include_router(test.router)

# ----- DATABASE -----
app.add_event_handler("startup", Database.connect_db)
app.add_event_handler("shutdown", Database.close_db)

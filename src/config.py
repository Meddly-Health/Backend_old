import json
import os


# ---------- UTIL FUNCTIONS ----------
def env_variable_to_dict(env_variable):
    try:
        return json.loads(env_variable)
    except json.JSONDecodeError:
        env_variable = env_variable.split(",")
        env_variable[0] = env_variable[0].replace("{", "")
        env_variable[-1] = env_variable[-1].replace("}", "")
        new_dict = {}

        for key_value in env_variable:
            key_value = key_value.split(":", 1)
            new_dict[key_value[0].strip()] = key_value[1].strip()

        return new_dict


# ---------- ENV VARIABLES ----------
db_string = os.getenv("MEDDLY_DB_STRING")
db_name = "Meddly"

firebase_json = env_variable_to_dict(os.getenv("MEDDLY_FIREBASE_JSON"))
firebase_private_key = os.getenv("MEDDLY_FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
firebase = {**firebase_json, "private_key": firebase_private_key}
firebase_key = os.getenv("MEDDLY_FIREBASE_KEY")
# ENV_NAME is the name of the environment. It can be "local-dev", "dev" or "prod"
env_name = os.getenv("MEDDLY_ENV_NAME")
sendgrid_key = os.getenv("MEDDLY_SENDGRID_KEY")
sendgrid_email = os.getenv("MEDDLY_SENDGRID_EMAIL")

# ---------- METADATA ----------
title = "Meddly"
version = 0.1
description = f"""
# Welcome to MeddlyApi!
![version](https://img.shields.io/badge/version-{version}-blue)  ![version](https://img.shields.io/badge/enviroment-{env_name.replace("-", "_")}-orange)

Created by:
- Cibello, Sofía Florencia
- Pieve Roiger, Ignacio
- Sala, Lorenzo
- Spini, Leila
"""

metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": "ignacio.pieve@gmail.com",
    },
    "description": description,
}

import json
import os

title = "Meddly"
version = 0.1
metadata = {
    "title": title,
    "version": version,
    "contact": {
        "name": f"{title} Team",
        "email": "ignacio.pieve@gmail.com",
    },
}


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


db_string = os.getenv("MEDDLY_DB_STRING")
db_name = "Meddly"

firebase_json = env_variable_to_dict(os.getenv("MEDDLY_FIREBASE_JSON"))
firebase_private_key = os.getenv("MEDDLY_FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
firebase = {**firebase_json, "private_key": firebase_private_key}
firebase_key = os.getenv("MEDDLY_FIREBASE_KEY")

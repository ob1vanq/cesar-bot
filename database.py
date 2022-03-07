import json
from pathlib import Path


class db:
    path_backup = Path().joinpath("db", "db_backup_copy.json")
    path = Path().joinpath("db", "db.json")

    @staticmethod
    def count():
        with open(db.path, "r") as file:
            data = list(json.load(file)["users_id"])
        return len(data)

    @staticmethod
    def add_user(user_id):
        with open(db.path, "r") as file:
            data = list(json.load(file)["users_id"])
        users = set(data)
        users.add(user_id)
        with open(db.path, "w") as file:
            json.dump(dict(users_id=list(users)), file, indent=4)

    @staticmethod
    def get_users():
        with open(db.path, "r") as file:
            data = list(json.load(file)["users_id"])
        return data

    @staticmethod
    def delete_user(user_id):
        with open(db.path, "r") as file:
            users = list(json.load(file)["users_id"])
        if user_id in users:
            users.remove(user_id)
            with open(db.path, "w") as file:
                json.dump(dict(users_id=list(users)), file, indent=4)

    @staticmethod
    def backup_copy():
        with open(db.path, "r") as file:
            data = json.load(file)

        with open(db.path_backup, "w") as file:
            json.dump(data, file, indent=4)
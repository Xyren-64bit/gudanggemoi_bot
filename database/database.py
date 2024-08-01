import pymongo, os
from config import DB_URL, DB_NAME

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]

user_data = database["users"]


async def present_user(user_id: int):
    found = user_data.find_one({"_id": user_id})
    return bool(found)


async def add_user(user_id: int):
    user_data.insert_one({"_id": user_id})
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc["_id"])

    return user_ids


async def del_user(user_id: int):
    user_data.delete_one({"_id": user_id})
    return


async def add_user_on_start(user_id: int):
    """
    Adds a user to the database when they send the /start command.

    Args:
        user_id: The user's ID.
    """

    if not await present_user(user_id):  # Check if the user is already in the database
        await add_user(user_id)

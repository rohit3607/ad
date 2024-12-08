#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return


# Admin functions

async def add_admin(user_id: int) -> bool:
    """Add a user to the admin list."""
    if admins_collection.find_one({"_id": user_id}):
        return False  # Admin already exists
    admins_collection.insert_one({"_id": user_id})
    return True


async def remove_admin(user_id: int) -> bool:
    """Remove a user from the admin list."""
    result = admins_collection.delete_one({"_id": user_id})
    return result.deleted_count > 0


async def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    admin = await admins_collection.find_one({"_id": user_id})
    return admin is not None


async def list_admins() -> list:
    """List all admins with detailed information."""
    from bot import Bot  # Late import to avoid circular dependency

    admins = admins_collection.find({})
    admin_list = []

    async for admin in admins:
        admin_id = admin["_id"]

        try:
            # Fetch user details using Bot.get_users
            admin_info = await Bot.get_users([admin_id])  # Pass admin_id as a list

            # Extract user information
            if admin_info:
                user = admin_info[0]  # Access the first (and only) user object
                username = user.username if user.username else user.first_name
                admin_list.append(f"{admin_id} - {username}")
            else:
                admin_list.append(f"{admin_id} - (No info found)")
        except Exception as e:
            admin_list.append(f"{admin_id} - Error: {str(e)}")

    return admin_list

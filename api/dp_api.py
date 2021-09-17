import motor.motor_asyncio
import requests
import api.config_api as capi

# Make request, for get current machine ip
r = requests.get("http://ip.42.pl/raw")
# Parse content
ip = r.text

DATABASE = capi.get_value(name="DATABASE")
# Make PyMongo client
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE)

# Get datebase from client
db = client["MagicNumberBot"]
# Get collection from database
users = db["users"]
# Indexing collection
# users.ensure_index([("UserID", 1), ("Email", 2)])

# Function for inderting data into collection
async def insert_db(db, data):
    # Sample: indert_db("users", {"username":"Denver"})
    #
    # db = string argument, name of collection
    # data = dict object with data
    #
    # Insert data to db, with parsing globals from arguments
    return await globals()[db].insert_one(data)

# Find in collection
async def find(db, idc=None, uname=None, mail=None, cusname=None, cusdata=None):
    # Sample: find("users", {"username":"Denver"})
    #
    # db = string argument, name of collection
    # idc = user ID code
    # uname = username
    # mail = user email address
    # cusname = custom key
    # cusdata = custom data
    #
    # You may change default values to own

    if uname:
        # Search in collection with username
        return await globals()[db].find_one({"username": uname})
    elif idc:
        # Search in collection with UserID
        return await globals()[db].find_one({"telegram_id": idc})
    elif mail:
        # Search in collection with Email
        return await globals()[db].find_one({"email": mail})
    elif cusdata and cusname:
        # Search in collection with custom key and custom data
        return await globals()[db].find_one({cusname: cusdata})

async def find_q(db, querry):
    # Sample: find_q("users", {"username":"Denver"})
    return await globals()[db].find_one(querry)

async def find_qa(db, querry):
    cursor =  globals()[db].find(querry)
    return await cursor.to_list(length=1000)
    
# Update value in collection
async def update_db(db, scdata, ndata):
    # Sample: update_db("users", {"username":"Denver"}, {"username":"DenverLaDePy"})
    #
    # db = string argument, name of collection
    # scdata = search/change data
    # ndata = username

    return await globals()[db].update_one(scdata, {"$set": ndata}, upsert=True)

# Delete object from collection
async def delete_db(db, obj):
    # Sample: delete_db("users", {"username":"DenverLaDePy"})
    await globals()[db].delete_one(obj)

# Checking if object in collection
async def is_used(db, idc=None, uname=None, mail=None, cusname=None, cusdata=None):
    # Sample: is_used("users", uname="Denver"})  return True/False
    #
    # db = string argument, name of collection
    # idc = user ID code
    # uname = username
    # mail = user email address
    # cusname = custom key
    # cusdata = custom data
    #
    # You may change default values to own
    if uname:
        return bool(await globals()[db].find_one({"username": uname}))
    elif idc:
        return bool(await globals()[db].find_one({"telegram_id": idc}))
    elif mail:
        return bool(await globals()[db].find_one({"email": mail}))
    elif cusdata and cusname:
        return bool(await globals()[db].find_one({cusname: cusdata}))
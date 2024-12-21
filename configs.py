from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

username = getenv("MONGO_USERNAME")
password = getenv("MONGO_PASSWORD")
host = getenv("MONGO_HOST")
port = int(getenv("MONGO_PORT"))
auth_db = getenv("MONGO_AUTH_DB")

uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_db}"
client = MongoClient(uri)
db = client["ipodb"]
pan_collection = db["pan"]
ipo_collection = db["ipo"]
ipo_pan_collection = db["ipo_pan"]

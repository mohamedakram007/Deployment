import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URI", "mongodb+srv://akrammohamed392005_db_user:<db_password>@cluster2.srig9zh.mongodb.net/?appName=Cluster2")

client = AsyncIOMotorClient(MONGO_URL)

db = client["products_db"]

product_collection = db["products"]

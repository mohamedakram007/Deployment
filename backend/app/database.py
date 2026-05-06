import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URI", "mongodb+srv://akrammohamed392005_db_user:jBu5x3MFkAYGyLmq@cluster1.hthsc2h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")

client = AsyncIOMotorClient(MONGO_URL)

db = client["products_db"]

product_collection = db["products"]
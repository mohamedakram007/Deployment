from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from .database import product_collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Backend Running Successfully"}

@app.get("/products")
async def get_products():
    try:
        raw_products = await product_collection.find().to_list(length=100)

        products = []

        for item in raw_products:
            item["_id"] = str(item["_id"])
            products.append(item)

        return products

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products"
        )

@app.post("/products")
async def create_product(product: dict):
    try:
        result = await product_collection.insert_one(product)

        return {
            "message": "Product added successfully",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to add product"
        )

@app.get("/products/{id}")
async def get_product(id: str):
    try:
        product = await product_collection.find_one(
            {"_id": ObjectId(id)}
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product["_id"] = str(product["_id"])

        return product

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID"
        )

@app.put("/products/{id}")
async def update_product(id: str, product: dict):
    try:
        result = await product_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": product}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not updated"
            )

        return {"message": "Product updated successfully"}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=400,
            detail="Update failed"
        )

@app.delete("/products/{id}")
async def delete_product(id: str):
    try:
        result = await product_collection.delete_one(
            {"_id": ObjectId(id)}
        )

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {"message": "Product deleted successfully"}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(
            status_code=400,
            detail="Delete failed"
        )

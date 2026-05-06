from fastapi import FastAPI, HTTPException
from .database import product_collection
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "MongoDB Connected"}

@app.get("/products")
async def get_products():
    print("DEBUG: [START] GET /products called")
    try:
        raw_products = await product_collection.find().to_list(length=100)
        products = []
        for item in raw_products:
            item["_id"] = str(item["_id"])
            products.append(item)
        print("DEBUG: [END] GET /products finished successfully")
        return products
    except Exception as e:
        print(f"DEBUG Error in GET /products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/{id}")
async def get_product(id: str):
    print(f"DEBUG: GET /products/{id} called")
    try:
        product = await product_collection.find_one({"_id": ObjectId(id)})
        if product:
            product["_id"] = str(product["_id"])
            return product
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        print(f"DEBUG Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.post("/products")
async def create_product(product: dict):
    print(f"DEBUG: POST /products called with data: {product}")
    try:
        result = await product_collection.insert_one(product)
        return {
            "message": "Product added",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        print(f"DEBUG Error: {e}")
        return {"error": str(e)}

@app.put("/products/{id}")
async def update_product(id: str, product: dict):
    print(f"DEBUG: PUT /products/{id} called with data: {product}")
    try:
        result = await product_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": product}
        )
        if result.modified_count == 1:
            return {"message": "Product updated successfully"}
        raise HTTPException(status_code=404, detail="Product not found or unchanged")
    except Exception as e:
        print(f"DEBUG Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/products/{id}")
async def delete_product(id: str):
    print(f"DEBUG: DELETE /products/{id} called")
    try:
        result = await product_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "Product deleted successfully"}
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        print(f"DEBUG Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

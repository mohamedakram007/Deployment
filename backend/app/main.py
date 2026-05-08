from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from bson.errors import InvalidId

from .database import product_collection

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://deployment-6tainovkm-mohamedakram007s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
async def home():
    return {"message": "MongoDB Connected Successfully"}

# Get All Products
@app.get("/products")
async def get_products():
    print("DEBUG: GET /products called")

    try:
        raw_products = await product_collection.find().to_list(length=100)

        products = []

        for item in raw_products:
            item["_id"] = str(item["_id"])
            products.append(item)

        print("DEBUG: Products fetched successfully")

        return products

    except Exception as e:
        print(f"DEBUG ERROR in GET /products: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products"
        )

# Get Single Product
@app.get("/products/{id}")
async def get_product(id: str):
    print(f"DEBUG: GET /products/{id}")

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

    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID"
        )

    except Exception as e:
        print(f"DEBUG ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch product"
        )

# Create Product
@app.post("/products")
async def create_product(product: dict):
    print(f"DEBUG: POST /products -> {product}")

    try:
        result = await product_collection.insert_one(product)

        return {
            "message": "Product added successfully",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print(f"DEBUG ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to create product"
        )

# Update Product
@app.put("/products/{id}")
async def update_product(id: str, product: dict):
    print(f"DEBUG: PUT /products/{id}")

    try:
        result = await product_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": product}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found or no changes made"
            )

        return {
            "message": "Product updated successfully"
        }

    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID"
        )

    except Exception as e:
        print(f"DEBUG ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to update product"
        )

# Delete Product
@app.delete("/products/{id}")
async def delete_product(id: str):
    print(f"DEBUG: DELETE /products/{id}")

    try:
        result = await product_collection.delete_one(
            {"_id": ObjectId(id)}
        )

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return {
            "message": "Product deleted successfully"
        }

    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID"
        )

    except Exception as e:
        print(f"DEBUG ERROR: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to delete product"
        )

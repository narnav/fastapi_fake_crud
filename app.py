from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Define CORS settings
origins = [
    "http://127.0.0.1:5500",  # Adjust for your frontend's URL
]

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the car
class Car(BaseModel):
    color: str
    brand: str
    price: float

# In-memory storage for simplicity (use a database in production)
fake_db = []

# CRUD Operations

# Create
@app.post("/cars/", response_model=Car)
async def create_car(car: Car):
    fake_db.append(car)
    return car

# Read All
@app.get("/cars/", response_model=List[Car])
async def get_cars():
    return fake_db

# Read One
@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int):
    if car_id >= len(fake_db):
        raise HTTPException(status_code=404, detail="Car not found")
    return fake_db[car_id]

# Update
@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, car: Car):
    if car_id >= len(fake_db):
        raise HTTPException(status_code=404, detail="Car not found")
    fake_db[car_id] = car
    return car

# Delete
@app.delete("/cars/{car_id}")
async def delete_car(car_id: int):
    if car_id >= len(fake_db):
        raise HTTPException(status_code=404, detail="Car not found")
    fake_db.pop(car_id)
    return {"message": "Car deleted successfully"}

# To run the FastAPI app, use: uvicorn app_name:app --reload

from typing import Union
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.waterdip


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TaskModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    is_completed: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


@app.post("/v1/tasks")
async def create_task(title: str):  # TODO
    # return a 201 code
    return {"id": 2}


@app.get("/v1/tasks")
async def get_all_task():  # TODO
    # return a 200 code
    return {"id": 2}


@app.get("/v1/tasks/{id}")
async def get_a_task(id: int):  # TODO
    # return a 200 code
    return {id: 3, "title": "Test Task 2", "is_completed": False}
    """
    if id not found:
    (return a 404 code)

    {
        error: "There is no task at that id"
    }
    """


@app.delete("/v1/tasks/{id}")
async def delete_a_task(id: int):  # TODO
    # return a 204 code
    return


@app.put("/v1/tasks/{id}")
async def delete_a_task(title: str, is_completed: bool):  # TODO
    # return a 204 code
    return
    """
    if id not found:
    (return a 404 code)

    {
        error: "There is no task at that id"
    }
    """

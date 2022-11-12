from fastapi import FastAPI, status, Body, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from schemas import *
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from typing import List, Any

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post("/v1/tasks", description="Create a new Task")
# async def create_task(tasks: CreateTaskModel = Body(...), db: Session = Depends(get_db)):
#     tasks = models.Task(title=tasks.title, is_completed=False)
#     db.add(tasks)
#     db.commit()
#     db.refresh(tasks)
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": tasks.id})


# @app.post("/v1/tasks", description="Create a new Task")
# async def create_task2(tasks: List[UpdateTaskModel] = Body(..., embed=True), db: Session = Depends(get_db)):
#     tasks = [models.Task(**task) for task in tasks]
#     db.add_all(tasks)
#     db.commit()
#     db.refresh(tasks)
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content={"tasks": jsonable_encoder([t.id for t in tasks])})


@app.post("/v1/tasks", description="Create a new Task")
async def create_task(body: Any = Body(...), db: Session = Depends(get_db)):
    if "tasks" in body:
        if isinstance(body["tasks"], list) and all([UpdateTaskModel.validate(task) for task in body["tasks"]]):
            body = [models.Task(**task) for task in body["tasks"]]
            db.add_all(body)
            db.commit()
            return JSONResponse(
                status_code=status.HTTP_201_CREATED, content={"tasks": jsonable_encoder([{"id": t.id} for t in body])}
            )
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid data"})
    else:
        if not CreateTaskModel.validate(body):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid data"})
        body = models.Task(title=body["title"], is_completed=False)
        db.add(body)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": body.id})


@app.get("/v1/tasks", description="List all tasks created")
async def get_all_task(db: Session = Depends(get_db)):
    all_tasks = db.query(models.Task).all()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"tasks": jsonable_encoder(all_tasks)})


@app.get("/v1/tasks/{id}", description="Get a specific task", response_model=TaskModel)
async def get_a_task(id: int, db: Session = Depends(get_db)):
    if (task := db.query(models.Task).filter(models.Task.id == id).first()) is not None:
        return task
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "There is no task at that id"})


@app.delete("/v1/tasks")
async def delete_bulk_tasks(tasks: List[GetTaskModel] = Body(..., embed=True), db: Session = Depends(get_db)):
    for task in tasks:
        db.query(models.Task).filter(models.Task.id == task.id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/v1/tasks/{id}")
async def delete_a_task(id: int, db: Session = Depends(get_db)):
    db.query(models.Task).filter(models.Task.id == id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/v1/tasks/{id}")
async def update_a_task(id: str, task: UpdateTaskModel = Body(...), db: Session = Depends(get_db)):

    if (db.query(models.Task).filter(models.Task.id == id).first()) is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "There is no task at that id"})

    update_result = db.query(models.Task).filter(models.Task.id == id).update(jsonable_encoder(task))
    db.commit()

    if update_result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

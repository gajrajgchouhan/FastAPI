from fastapi import FastAPI, status, Body, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from schemas import *
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/v1/tasks", description="Create a new Task")
async def create_task(task: CreateTaskModel, db: Session = Depends(get_db)):
    task = models.Task(title=task.title, is_completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": task.id})


@app.get("/v1/tasks", description="List all tasks created")
async def get_all_task(db: Session = Depends(get_db)):
    all_tasks = db.query(models.Task).all()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"tasks": jsonable_encoder(all_tasks)})


@app.get("/v1/tasks/{id}", description="Get a specific task", response_model=TaskModel)
async def get_a_task(id: int, db: Session = Depends(get_db)):
    if (task := db.query(models.Task).filter(models.Task.id == id).first()) is not None:
        return task
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "There is no task at that id"})


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

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query,status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from typing import Optional
from app.models.task import StatusEnum, PriorityEnum, Task
from app.schemas.task import TaskListOut
from app.dependencies import get_current_user
router= APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


#create new task
@router.post("/",response_model=schemas.TaskOut,status_code=status.HTTP_201_CREATED)
def createPost(payload:schemas.TaskCreate,db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    new_task=models.Task(**payload.model_dump(exclude={"user_id"}), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#get all tasks
@router.get("/",response_model=List[schemas.TaskOut])
def getAllTasks(db:Session=Depends(get_db), current_user = Depends(get_current_user)):  
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    return tasks


#get task by id
@router.get("/{task_id}",response_model=schemas.TaskOut,)
def getTask(task_id:int,db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    return task



#update task by id
@router.patch("/{task_id}",response_model=schemas.TaskOut)
def updateTask(task_id:int, payload:schemas.TaskUpdate, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

#delete task by id
@router.delete("/{task_id}", response_model=dict, status_code=status.HTTP_200_OK)
def deleteTask(task_id:int, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
    


#get tasks with pagination, filtering by status and priority
@router.get("/pagination",response_model=TaskListOut)
def get_tasks(
    skip:int=Query(default=0,ge=0),
    limit:int=Query(default=10,ge=1,le=100),
    status:Optional[StatusEnum]=Query(default=None),
    priority:Optional[PriorityEnum]=Query(default=None),
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if status is not None:
        query= query.filter(Task.status == status)
    if priority is not None:
        query= query.filter(Task.priority == priority)      

    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    
    return TaskListOut(total=total, skip=skip, limit=limit, tasks=tasks)

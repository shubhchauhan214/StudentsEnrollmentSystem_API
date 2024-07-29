from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from pydantic import BaseModel, Field

from models import Student

router=APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


class StudentRequest(BaseModel):
    name: str = Field(..., example="Shubham Chauhan")
    email: str = Field(..., example="shubham.chauhan@example.com")


# POST METHOD// Create new student
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(db: db_dependency, student_request: StudentRequest):
    student_model = Student(**student_request.dict())

    db.add(student_model)
    db.commit()


# Get all Data
@router.get("/student", status_code=status.HTTP_200_OK)
async def read_students(db: db_dependency):
    return db.query(Student).all()


# Read data using id
@router.get("/student/{student_id}", status_code=status.HTTP_200_OK)
async def read_students_id(db:db_dependency, student_id: int = Path(gt=0)):
    student_model = db.query(Student).filter(Student.id == student_id).first()
    if student_model is not None:
        return student_model
    raise HTTPException(status_code=404, detail='Student not found')



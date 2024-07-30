from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from database import get_db
from models import Course

router=APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


class CourseRequest(BaseModel):
    name: str = Field(..., example='Math 101')
    description = Optional[str] = Field(None, example="Basic Math Course")


# POST METHOD// Create new student
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_student(db: db_dependency, course_request: CourseRequest):
    student_model = Course(**course_request.dict())

    db.add(student_model)
    db.commit()


# Get all Data
@router.get("/course", status_code=status.HTTP_200_OK)
async def all_courses(db: db_dependency):
    return db.query(Course).all()


# Read data using id
@router.get("/course/{course_id}", status_code=status.HTTP_200_OK)
async def course_by_id(db: db_dependency, course_id: int = Path(gt=0)):
    course_model = db.query(Course).filter(Course.id == course_id).first()
    if course_model is not None:
        return course_model
    raise HTTPException(status_code=404, detail='Course not available')


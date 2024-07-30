from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Path
from models import Course, Enrollment, Student
from database import get_db

router = APIRouter()


class CourseBase(BaseModel):
    name: str = Field(..., example="Math 101")
    description: Optional[str] = Field(None, example="Basic Math Course")


class CourseCreate(CourseBase):
    pass


class CourseOut(CourseBase):  # Adding CourseOut model
    id: int

    class Config:
        orm_mode = True


@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(name=course.name, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", response_model=List[CourseOut])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Course).offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=CourseOut)
def read_course(course_id: int = Path(..., title="The ID of the course to retrieve", gt=0), db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return db_course

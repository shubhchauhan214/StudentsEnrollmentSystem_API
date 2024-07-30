from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from pydantic import BaseModel, Field

from models import Enrollment, Student, Course

router = APIRouter()


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


@router.post("/", status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


@router.delete("/")
def drop_student(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).delete()
    db.commit()
    return {"detail": "Enrollment removed"}


@router.get("/students/{student_id}/courses/", response_model=List[Course])
def get_student_courses(student_id: int = Path(..., title="The ID of the student to retrieve courses for", gt=0)\
                        , db: Session = Depends(get_db)):
    return db.query(Course).join(Enrollment).filter(Enrollment.student_id == student_id).all()


@router.get("/courses/{course_id}/students/", response_model=List[Student])
def get_course_students(course_id: int = Path(..., title="The ID of the course to retrieve students for", gt=0)\
                        , db: Session = Depends(get_db)):
    return db.query(Student).join(Enrollment).filter(Enrollment.course_id == course_id).all()



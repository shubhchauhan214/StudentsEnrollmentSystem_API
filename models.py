from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # Relationship with courses via enrollments
    enrolled_courses = relationship("Course", secondary="enrollments", back_populates="enrolled_students")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    available_seats = Column(Integer)

    # Relationship with students via enrollments
    enrolled_students = relationship("Student", secondary="enrollments", back_populates="enrolled_courses")

class Enrollment(Base):
    __tablename__ = 'enrollments'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
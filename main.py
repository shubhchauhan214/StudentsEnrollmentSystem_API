from fastapi import FastAPI
from database import engine, Base
from routers import students, enrollments, courses

# Create the FastAPI app
app = FastAPI()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])

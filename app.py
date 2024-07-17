from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Import models and database connection
from database import SessionLocal, engine
import models

# Create database and tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class StudentInformationBase(BaseModel):
    first_name: str
    last_name: str
    student_id: int
    birth_date: str
    gender: str

class StudentInformationCreate(StudentInformationBase):
    pass

class StudentInformationUpdate(StudentInformationBase):
    pass

class StudentInformation(StudentInformationBase):
    id: int

    class Config:
        orm_mode = True

# API endpoints
@router_v1.get('/student_information', response_model=List[StudentInformation])
async def get_student_information(db: Session = Depends(get_db)):
    return db.query(models.StudentInformation).all()

@router_v1.get('/student_information/{student_id}', response_model=StudentInformation)
async def get_student_information(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.StudentInformation).filter(models.StudentInformation.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router_v1.post('/student_information', response_model=StudentInformation, status_code=201)
async def create_student_information(student: StudentInformationCreate, db: Session = Depends(get_db)):
    db_student = models.StudentInformation(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router_v1.put('/student_information/{student_id}', response_model=StudentInformation)
async def update_student_information(student_id: int, student: StudentInformationUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.StudentInformation).filter(models.StudentInformation.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@router_v1.delete('/student_information/{student_id}', status_code=204)
async def delete_student_information(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.StudentInformation).filter(models.StudentInformation.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return Response(status_code=204)

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

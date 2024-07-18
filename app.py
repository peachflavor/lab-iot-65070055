from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

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

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(response: Response, book_id: int, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not found'
        }
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation

    if 'title' not in book or 'author' not in book or 'year' not in book or 'is_published' not in book:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Book).filter(models.Book.title == book['title']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Book already exists'
        }

    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(response: Response, book_id: int, book: dict, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not exists'
        }
    db.query(models.Book).filter(models.Book.id == book_id).update(book)
    db.commit()
    return {
        'message': 'Book updated'
    }

@router_v1.delete('/books/{book_id}')
async def delete_book(response: Response, book_id: int, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not exists'
        }

    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()
    return {
        'message': 'Book deleted'
    }

# Students

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_student(response: Response, student_id: int, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not found'
        }
    return db.query(models.Student).filter(models.Student.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):

    if 'firstname' not in student or 'lastname' not in student or 'dob' not in student or 'id' not in student:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Student).filter(models.Student.id == student['id']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Student already exists'
        }

    newstudent = models.Student(firstname = student['firstname'], lastname = student['lastname'], dob = student['dob'], id = student['id'], gender = student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.delete('/students/{student_id}')
async def delete_student(response: Response, student_id: int, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not exists'
        }
    db.query(models.Student).filter(models.Student.id == student_id).delete()
    db.commit()
    return {
        'message': 'Student deleted'
    }

@router_v1.patch('/students/{student_id}')
async def update_student(response: Response, student_id: int, student: dict, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not exists'
        }
    db.query(models.Student).filter(models.Student.id == student_id).update(student)
    db.commit()
    return {
        'message': 'Student updated'
    }

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

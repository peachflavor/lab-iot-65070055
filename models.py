from sqlalchemy import Boolean, Column, Date, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class StudentInformation(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    gender = Column(String)


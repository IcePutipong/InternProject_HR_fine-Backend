from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from models.timesheet_model import TimeStamp

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    
    emp_id = Column(String(100), unique=True, nullable=False) ###employeeID
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    create_year = Column(Integer)
    reset_status = Column(Boolean, default=False)

    personal_info = relationship("PersonalInfo", back_populates="user", uselist=False)
    address_info = relationship("AddressInfo", back_populates="user", uselist=False)
    registration_address = relationship("RegistrationAddress", back_populates="user", uselist=False)
    hiring_info = relationship("HiringInfo", back_populates="user", uselist=False)
    payment_info = relationship("PaymentInfo", back_populates="user", uselist=False)
    contact_info = relationship("ContactInfo", back_populates="user", foreign_keys="[ContactInfo.emp_id]", uselist=False)
    deduction_info = relationship("DeductionInfo", back_populates="user", uselist=False)

    time_stamp = relationship("TimeStamp", back_populates="user")
    
class RefreshToken(Base):
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey(Users.id))
    access_token = Column(String(450), nullable=False)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)

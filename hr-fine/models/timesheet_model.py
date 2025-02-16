from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

AUTH_USER_EMP_ID = "users.emp_id"

class TimeStamp(Base):
    __tablename__ = "time_stamp"
    stamp_id = Column(Integer, primary_key=True, index=True)

    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False)
    project_id = Column(Integer, ForeignKey("project_details.project_id"), nullable=False)
    
    stamp_date = Column(Date, nullable=False)
    start_time = Column(String(20), nullable=False)
    end_time = Column(String(20), nullable=False)
    stamp_details = Column(String(300), nullable=True)
    disbursement = Column(Boolean, nullable=False)
    OverTime = Column(Boolean, nullable=False)
    travel_expenses = Column(Boolean, nullable=False)

    user = relationship("Users", back_populates="time_stamp")
    project = relationship("ProjectDetails", back_populates="project_progress")
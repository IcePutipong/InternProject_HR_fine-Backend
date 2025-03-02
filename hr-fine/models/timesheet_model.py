from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from database.db import Base

AUTH_USER_EMP_ID = "users.emp_id"

class TimeStamp(Base):
    __tablename__ = "time_stamp"
    stamp_id = Column(Integer, primary_key=True, index=True)

    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False)
    project_id = Column(Integer, ForeignKey("project_details.project_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("project_plan.id"), nullable=True)
    
    stamp_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    total_time = Column(Time, nullable=True)
    stamp_details = Column(String(1000), nullable=True)

    disbursement = Column(Boolean, nullable=False)
    OverTime = Column(Boolean, nullable=False)
    travel_expenses = Column(Boolean, nullable=False)

    user = relationship("Users", back_populates="time_stamp")
    project = relationship("ProjectDetails", back_populates="project_progress")
    period = relationship("ProjectPlan", back_populates="period_progress")
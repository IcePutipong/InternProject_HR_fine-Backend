from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey, Float, Double
from database.db import Base
from sqlalchemy.orm import relationship
from models.client_model import Client

PROJECT_ID = "project_details.project_id"

class ProjectDetail(Base):
    __tablename__ = "project_details"
    project_id = Column(Integer, primary_key=True, index=True)

    project_code = Column(String(10), nullable=False)
    project_name = Column(String(30), nullable=False)
    project_contract_no = Column(String(20), nullable=False)
    project_details = Column(String(100), nullable=True)

    project_client = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    project_manager = Column(Integer, ForeignKey("personal_info.id"), nullable=False)
    color_mark = Column(String(10), nullable=False)

    client = relationship("Client", back_populates="project_details")
    manager = relationship("PersonalInfo", back_populates="managed_projects")

class ProjectDuration(Base): 
    __tablename__ = "project_duration"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    project_duration = Column(Integer, nullable=False)
    project_sign_date = Column(Date, nullable=False)
    project_end_date = Column(Date, nullable=False)

class ProjectBill(Base):
    __tablename__ = "project_bill"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    billable = Column(Boolean, nullable=False)
    project_value = Column (Double, nullable=False)
    project_billing_rate = Column(Double, nullable=False)


class ProjectPlan(Base):
    __tablename__ = "project_plan"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    period_no = Column(Integer, nullable=False)
    deli_duration = Column(Date, nullable=False)
    deli_date = Column(Date, nullable=False)
    deli_details = Column(String(100), nullable=True)

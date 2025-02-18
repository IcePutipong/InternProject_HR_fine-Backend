from datetime import date, datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey, Float, Double
from database.db import Base
from sqlalchemy.orm import relationship

PROJECT_ID = "project_details.project_id"

class ProjectDetails(Base):
    __tablename__ = "project_details"
    project_id = Column(Integer, primary_key=True, index=True)


    project_type = Column(Integer, ForeignKey("project_types.id"), nullable=False)
    project_code = Column(String(10), nullable=False)
    project_name = Column(String(30), nullable=False)
    project_contract_no = Column(String(20), nullable=False)
    project_details = Column(String(100), nullable=True)

    project_client = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    project_manager = Column(String(100), ForeignKey("users.emp_id"), nullable=False)
    color_mark = Column(String(10), nullable=False)

    client = relationship("Client", back_populates="project_details")
    manager = relationship("Users", back_populates="managed_projects")
    project_types = relationship("ProjectType", back_populates="project" , uselist=True)
    project_progress = relationship("TimeStamp", back_populates="project")

    project_duration = relationship("ProjectDuration", back_populates="project", uselist=False)
    project_bill = relationship("ProjectBill", back_populates="project", uselist=False)
    project_plan = relationship("ProjectPlan", back_populates="project", uselist=True)
    project_members = relationship("ProjectMember", back_populates="project")


class ProjectDuration(Base):
    __tablename__ = "project_duration"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    number_of_periods = Column(Integer, nullable=False)
    project_duration = Column(Integer, nullable=False)
    project_sign_date = Column(Date, nullable=False)
    project_end_date = Column(Date, nullable=False)

    project = relationship("ProjectDetails", back_populates="project_duration")

class ProjectBill(Base):
    __tablename__ = "project_bill"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    billable = Column(Boolean, nullable=False)
    project_value = Column (Double, nullable=False)
    project_billing_rate = Column(Double, nullable=False)

    project = relationship("ProjectDetails", back_populates="project_bill")


class ProjectPlan(Base):
    __tablename__ = "project_plan"
    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    period_no = Column(Integer, nullable=False)
    deli_duration = Column(Integer, nullable=False)
    deli_date = Column(Date, nullable=False)
    deli_details = Column(String(300), nullable=True)

    project = relationship("ProjectDetails", back_populates="project_plan")

class ProjectMember(Base):
    __tablename__ = "project_member"
    project_member_id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey(PROJECT_ID), nullable=False)
    member_id = Column(String(100), ForeignKey("users.emp_id"), nullable=False)
    position_id = Column(Integer, ForeignKey("hiring_info.position"), nullable=False)

    assigned_date = Column(Date, default=date.today)
    assigned_detail = Column(String(200), nullable=True)

    project = relationship("ProjectDetails", back_populates="project_members")
    member = relationship("Users", back_populates="project_members")
    member_position = relationship("HiringInfo", back_populates="project_members_position")

class ProjectType(Base):
    __tablename__ = "project_types"
    id = Column(Integer, primary_key=True, index=True)
    project_types = Column(String(20), nullable=False)
    
    client = relationship("Client", back_populates="client_types")
    project = relationship("ProjectDetails", back_populates="project_types")
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey, Float, Double
from database.db import Base
from sqlalchemy.orm import relationship
from models.project_model import ProjectDetails

AUTH_USER_EMP_ID = "users.emp_id"

class PersonalInfo(Base):
    __tablename__ = "personal_info"
    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)

    nation_id = Column(String(50), nullable=False)

    thai_name = Column(String(100), nullable=False)
    eng_name = Column(String(100), nullable=False)
    thai_nickname = Column(String(50), nullable=False)
    eng_nickname = Column(String(50), nullable=False)

    gender = Column(String(50), nullable=False)
    nation = Column(String(100), nullable=False)
    religion = Column(String(50), nullable=True)
    date_birth = Column(Date, nullable=True)

    user = relationship("Users", back_populates="personal_info")
    managed_projects = relationship("ProjectDetails", back_populates="manager")


class AddressInfo(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index= True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)
    house_no = Column(String(20), nullable=False)
    village_no = Column(Integer, nullable=False)
    sub_district = Column(String(50), nullable= False)
    district = Column(String(50), nullable= False)
    province = Column(String(50), nullable=False)
    zipcode = Column(String(20), nullable= False)
    country = Column(String(50), nullable=False)

    room_no = Column(Integer, nullable=True)
    floor = Column(Integer, nullable=True)
    village = Column(String(50), nullable=True)
    building = Column(String(50), nullable=True)
    alley = Column(String(50), nullable=True)
    road = Column(String(50), nullable=True)

    user = relationship("Users", back_populates="address_info")

class RegistrationAddress(Base):
    __tablename__ = "registration_address"
    id = Column(Integer, primary_key=True, index= True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)

    house_no = Column(String(20), nullable=False)
    village_no = Column(Integer, nullable=False)
    sub_district = Column(String(50), nullable= False)
    district = Column(String(50), nullable= False)
    province = Column(String(50), nullable=False)
    zipcode = Column(String(20), nullable= False)
    country = Column(String(50), nullable=False)

    room_no = Column(String(10), nullable=True)
    floor = Column(Integer, nullable=True)
    village = Column(String(50), nullable=True)
    building = Column(String(50), nullable=True)
    alley = Column(String(50), nullable=True)
    road = Column(String(50), nullable=True)

    user = relationship("Users", back_populates="registration_address")

class ContactInfo(Base):
    __tablename__ = "contact_info"
    id = Column(Integer, primary_key=True, index= True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)
    email = Column(String(100), ForeignKey("users.email"), nullable= False)

    tel = Column(String(15), nullable=False)
    line_id = Column(String(50), nullable=False)

    user = relationship("Users", back_populates="contact_info", foreign_keys=[emp_id])

class HiringInfo(Base):
    __tablename__ = "hiring_info"
    id = Column(Integer, primary_key=True, index= True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False)

    start_date = Column(Date, nullable=False)
    working_status = Column(String(20), nullable=False)
    prodation_date = Column(Date, nullable=False)
    terminate_date = Column(Date, nullable=False)
    
    emp_type = Column(String(50), nullable=False)
    working_location = Column(String(50), nullable=False)
    contract_type = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    manager = Column(String(100), nullable=False)

    user = relationship("Users", back_populates="hiring_info")
    
class PaymentInfo(Base):
    __tablename__ = "payment_info"
    id = Column(Integer, primary_key=True, index= True)
    emp_id = Column(String(100), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)

    payment_type = Column(String(50), nullable=False)
    account_no = Column(String(20), nullable=True)
    bank = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)

    user = relationship("Users", back_populates="payment_info")

class DeductionInfo(Base):
    __tablename__ = "deduction_info"
    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(String(50), ForeignKey(AUTH_USER_EMP_ID), nullable=False, unique=True)

    deduct_social_security = Column(Boolean, nullable=False)
    social_security_company = Column(String(50), nullable=True)
    social_security_emp_percentage= Column(Float, nullable=True)
    social_security_company_percentage = Column(Float, nullable=True)
    enroll_date = Column(Date, nullable=True)
    pri_healthcare = Column(String(50), nullable=True)
    sec_healthcare = Column(String(50), nullable=True)
    provide_fund_percentage = Column(Float, nullable=True)
    fee = Column(Float, nullable=True)

    has_social_security = Column(Boolean, nullable= False)
    establishment_location = Column(String(50), nullable=True)
    deduct_SLF_IC = Column(Boolean, nullable=True)
    pay_SLF_IC = Column(Float, nullable=True)

    has_other_details = Column(Boolean, nullable=False)
    other_details = Column(String(100), nullable=True)
    other_expenses = Column(Float, nullable=True)
    other_percentage = Column(Float, nullable= True)

    user = relationship("Users", back_populates="deduction_info", foreign_keys=[emp_id])

class Company(Base):
    __tablename__ = "company_location"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(50), nullable=False)

class EmployeeType(Base):
    __tablename__ = "emp_type"
    id = Column(Integer, primary_key=True, index=True)
    employee_type = Column(String(50), nullable=False)

class ContractType(Base): 
    __tablename__ = "contract_type"
    id = Column(Integer, primary_key=True, index=True)
    contract_type = Column(String(50), nullable=False)


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(50), nullable=False)
    positions = relationship("Position", back_populates="department")
    

class Position(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department = relationship("Department", back_populates="positions")
 
class WorkingStatus(Base):
    __tablename__ = "working_status"
    id = Column(Integer, primary_key=True, index=True)
    working_status = Column(String(50), nullable=False)

    


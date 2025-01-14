from fastapi import HTTPException, Depends
from typing import Any, Dict
from sqlalchemy.orm import Session
from schemas.optional_schema import (
    AddCompany, AddEmployeeType, AddContractType, AddDepartment, AddPosition, AddWorkingStatus
)
from models.user_model import Company, EmployeeType, ContractType, Department, Position, WorkingStatus
from database.db import get_session

def update_model_data(model, data: Dict):
    for key, value in data.items():
        setattr(model, key, value)

def add_company(request: AddCompany, db: Session=Depends(get_session)):
    existing_company = db.query(Company).filter(Company.company == request.company).first()
    if existing_company:
        raise HTTPException(status_code=400, detail="Company Already exists.")

    new_company = Company(
        company=request.company,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return{
        "company": new_company
    }

def add_employee_type(request: AddEmployeeType, db: Session=Depends(get_session)):
    existing_emp_type = db.query(EmployeeType).filter(EmployeeType.employee_type == request.employee_type).first()
    if existing_emp_type:
        raise HTTPException(status_code=400, detail="Employee type already exists.")
   
    new_employee_type = EmployeeType(
        employee_type = request.employee_type,
    )

    db.add(new_employee_type)
    db.commit()
    db.refresh(new_employee_type)
    return{
        "employee_type": new_employee_type
    }

def add_contract_type(request: AddContractType, db: Session=Depends(get_session)):
    existing_contract_type = db.query(ContractType).filter(ContractType.contract_type == request.contract_type).first()
    if existing_contract_type:
        raise HTTPException(status_code=400, detail="Contract type already exists.")

    new_contract_type = ContractType(
        contract_type = request.contract_type,
    )

    db.add(new_contract_type)
    db.commit()
    db.refresh(new_contract_type)
    return{
        "contract_type": new_contract_type
    }

def add_department(request: AddDepartment, db: Session=Depends(get_session)):
    existing_department = db.query(Department).filter(Department.department == request.department).first()
    if existing_department: 
        raise HTTPException(status_code=400, detail="Department already exists.")

    new_department = Department(
        department = request.department,
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return{
        "id": new_department.id,
        "department": new_department
    }

def add_position(request: AddPosition, db: Session=Depends(get_session)):
    existing_position = db.query(Position).filter(Position.position == request.position, Position.department_id == request.department_id).first()
    if existing_position:
        raise HTTPException(status_code=400, detail="Position already exist.")
    
    department = db.query(Department).filter(Department.id == request.department_id).first()
    if not department: 
        raise HTTPException(status_code=404, detail="Department not found")

    new_position = Position(
        position = request.position,
        department_id = request.department_id
    )

    db.add(new_position)
    db.commit()
    db.refresh(new_position)

    return {
        "id": new_position.id,
        "position": new_position.position,
        "department_id": new_position.department_id
    }

def add_working_status(request: AddWorkingStatus, db: Session=Depends(get_session)):
    existing_working_status = db.query(WorkingStatus).filter(WorkingStatus.working_status == request.working_status).first()
    if existing_working_status: 
        raise HTTPException(status_code=400, detail="Working Status Already exists.")
    
    new_working_status = WorkingStatus(
        working_status = request.working_status
    )

    db.add(new_working_status)
    db.commit()
    db.refresh(new_working_status)

    return{
        "working_status": new_working_status
    }

def edit_position(request: AddPosition, db: Session = Depends(get_session)):
    position = db.query(Position).filter(Position.id == request.id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found.")
    
    existing_position = db.query(Position).filter(
        Position.position == request.position,
        Position.department_id == request.department_id,
        Position.id != request.id
    ).first()
    if existing_position:
        raise HTTPException(status_code=400, detail="Position with the same name already exist in this department.")
    
    position.position = request.position
    position.department_id = request.department_id
    db.commit()
    db.refresh(position)

    return {
        "id": position.id,
        "position": position.position,
        "department_id": position.department_id
    }
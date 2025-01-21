from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.exc import NoResultFound

from models.client_model import Client
from models.project_model import ProjectDetails, ProjectBill, ProjectDuration, ProjectPlan, ProjectType
from services.user_service import update_model_data

from schemas.project_schema import CreateProject, CreateProjectPlan, GenerateProjectCode
from schemas.optional_schema import AddProjectType

def generate_project_code(request: GenerateProjectCode, db: Session = Depends(get_session)):
    try: 
        client = db.query(Client).filter(Client.client_name == request.client_name).one()
        client_code = client.client_project_code
        client_project_type = client.client_type
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Invalid client name or no client found")
    
    if client_project_type != request.project_type:
        raise HTTPException(
            status_code=400,
            detail=f"Project type mismatch: Client '{request.client_name}' is associated with '{client_project_type}', not '{request.project_type}'."
        )
    
    prefix = client_code

    existing_code = db.query(ProjectDetails.project_code).filter(
        ProjectDetails.project_code.like(f"{prefix}-%")
    ).all()

    existing_number = [int(code.split('-')[-1]) for code, in existing_code]
    next_number = max(existing_number, default=0) +1

    project_code = f"{prefix}-{next_number:03d}"
    return{"project-code": project_code}

def create_project(request: CreateProject, db: Session=Depends(get_session)):
    
    new_project_details = ProjectDetails(
        project_type = request.project_details.proect_type,
        project_code = request.project_details.project_code,
        project_name = request.project_details.project_name,
        project_contract_no = request.project_details.project_contract_no,
        project_details = request.project_details.project_details,
        project_client = request.project_details.project_client,
        project_manager = request.project_details.project_manager,
        color_mark =request.project_details.color_mark,
    )
    db.add(new_project_details)

    new_project_duration = ProjectDuration(
        project_id = request.project_duration.project_id,
        project_duration = request.project_duration.project_duration,
        project_sign_date = request.project_duration.project_sign_date,
        project_end_date = request.project_duration.project_end_date

    )
    db.add(new_project_duration)

    new_project_bill = ProjectBill(
        project_id = request.project_bill.project_id,
        billable = request.project_bill.billable,
        project_value =request.project_bill.project_value,
        project_billing_rate = request.project_bill.project_billing_rate,
    )
    db.add(new_project_bill)

    db.commit()
    db.refresh(new_project_details)
    db.refresh(new_project_duration)
    db.refresh(new_project_bill)

    return{
        "project_details": new_project_details,
        "project_duration": new_project_duration,
        "project_bill": new_project_bill,
    }







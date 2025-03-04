from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.exc import NoResultFound
from pydantic import TypeAdapter

from models.client_model import Client
from models.project_model import ProjectDetails, ProjectBill, ProjectDuration, ProjectMember, ProjectPlan, ProjectType
from models.auth_model import Users
from models.user_model import HiringInfo, PersonalInfo, Position

from services.user_service import update_model_data

from schemas.project_schema import GenerateProjectCode, ProjectAllDetails, ProjectAssigned, ProjectBillBase, ProjectDetailsBase, ProjectDurationBase, ProjectMemberBase, ProjectPlanBase, SubmitallProjectData, ProjectDashboardinfo
from schemas.optional_schema import AddProjectType

from utils.jwt_bearer import JWTBearer, decode_jwt

from constants import EMP_ID_NOT_EXIST

def update_model_data(model, data: Dict):
    for key, value in data.items():
        setattr(model, key, value)

def generate_project_code(request: GenerateProjectCode, db: Session = Depends(get_session)):
    try: 
        client = db.query(Client).filter(Client.client_id == request.client_id).one()
        client_code = client.client_code
        client_project_type = client.client_type
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Invalid client name or no client found")
    
    # if request.project_type != client_project_type:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Project type mismatch: Client '{request.client_name}' is associated with '{client_project_type}', not '{request.project_type}'."
    #     )
    
    prefix = client_code

    existing_code = db.query(ProjectDetails.project_code).filter(
        ProjectDetails.project_code.like(f"{prefix}-%")
    ).all()

    existing_number = [int(code.split('-')[-1]) for code, in existing_code]
    next_number = max(existing_number, default=0) +1

    project_code = f"{prefix}-{next_number:03d}"
    return{"project-code": project_code}

def create_project_details(db: Session, project_details_data: dict):

    project_code = project_details_data.get("project_code")

    existing_porject_code = db.query(ProjectDetails).filter(ProjectDetails.project_code == project_code).first()

    if existing_porject_code:
        raise HTTPException(status_code=400, detail=f"Project code '{project_code}' already exists. Please use a unique code.")


    project_manage_id = project_details_data.get("project_manager")
    employee = db.query(Users).filter(Users.emp_id == project_manage_id).first()
    
    if not employee: 
        raise HTTPException(status_code=400, detail="Invalid project manager. Employee does not exist.")

    db_project_details = ProjectDetails(**project_details_data)
    db.add(db_project_details)
    db.commit()
    db.refresh(db_project_details)
    return db_project_details

def create_project_duration(db: Session, project_id: int, project_duretion_data: dict):
    project_duretion_data["project_id"] = project_id
    db_project_duration = ProjectDuration(**project_duretion_data)
    db.add(db_project_duration)
    db.commit()
    db.refresh(db_project_duration)
    return db_project_duration

def create_project_bill(db:Session, project_id: int, project_bill_data: dict):
    project_bill_data["project_id"]  =project_id
    db_project_bill = ProjectBill(**project_bill_data)
    db.add(db_project_bill)
    db.commit()
    db.refresh(db_project_bill)
    return(db_project_bill)

def create_project_member(db: Session, project_id: int, project_member_data: dict):

    member_id = project_member_data.get("member_id")
    project_member = db.query(Users).filter(Users.emp_id == member_id).first()

    if not project_member:
        raise HTTPException(status_code=400, detail="Invalid project member. Employee does not exist.")

    hiring_info = db.query(HiringInfo).filter(HiringInfo.emp_id == member_id).first()

    if not hiring_info:
        raise HTTPException(status_code=400, detail="No hiring info found for this employee.")

    project_member_data["position_id"] = hiring_info.position  
    project_member_data["project_id"] = project_id

    db_project_member = ProjectMember(**project_member_data)
    db.add(db_project_member)
    db.commit()
    db.refresh(db_project_member)
    
    return db_project_member


def create_project_plan(db: Session, project_id: int, project_plan_data: dict):
    project_plan_data["project_id"]= project_id
    db_project_plan = ProjectPlan(**project_plan_data)
    db.add(db_project_plan)
    db.commit()
    db.refresh(db_project_plan)
    return db_project_plan

def process_model_creation(
    db: Session,
    project_id: str,
    model_cls,
    existing_query_cls,
    creation_func,
    data_dict: dict,
    model_name: str,
):
    try:
        if model_name not in ["Project Plan", "Project Member"]:
            existing_data = db.query(existing_query_cls).filter(
                existing_query_cls.project_id == project_id
            ).first()

            if existing_data:
                return {
                    "status": "skip",
                    "message": f"{model_name} with project_id '{project_id}' already exists. Skipping."
                }

        new_data = creation_func(db, project_id, data_dict)
        return {
            "status": "success",
            "data": new_data.__dict__
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "error": f"Error creating {model_name}: {str(e)}"
        }

    
def process_all_sections(
        db: Session,
        project_id: str,
        data_sections: List[Dict[str, Any]]
):
    responses = {}
    for section in data_sections:
        if section["data_dict"]:
            responses[section["model_name"]] = process_model_creation(
                db=db,
                project_id=project_id,
                model_cls=section["model_cls"],
                existing_query_cls=section["existing_query_cls"],
                creation_func=section["creation_func"],
                data_dict=section["data_dict"],
                model_name=section["model_name"]
            )
    return responses

def submit_all_project_data(db: Session, data: SubmitallProjectData) -> dict:
    try:
        project_info = data.projectInfo

        if not project_info or not project_info.project_details:
            return {"status": "error", "error": "Missing required project details."}

        project_details_data = project_info.project_details.model_dump()
        created_project = create_project_details(db, project_details_data)
        project_id = created_project.project_id

        data_sections = []

        if project_info.project_duration:
            project_duration_data = project_info.project_duration.model_dump()
            created_duration = create_project_duration(db, project_id, project_duration_data)
            number_of_periods = created_duration.number_of_periods

            data_sections.append({
                "data_dict": project_duration_data,
                "model_cls": ProjectDuration,
                "existing_query_cls": ProjectDuration,
                "creation_func": create_project_duration,
                "model_name": "Project Duration"
            })

        if project_info.project_bill:
            data_sections.append({
                "data_dict": project_info.project_bill.model_dump(),
                "model_cls": ProjectBill,
                "existing_query_cls": ProjectBill,
                "creation_func": create_project_bill,
                "model_name": "Project Bill"
            })

        if data.projectPlanInfo and data.projectPlanInfo.project_plan:
            project_plans = data.projectPlanInfo.project_plan

            if len(project_plans) != number_of_periods:
                return {
                    "status": "error",
                    "error": f"Number of project plans ({len(project_plans)}) does not match the number of periods ({number_of_periods})."
                }

            for plan in project_plans:
                data_sections.append({
                    "data_dict": plan.model_dump(),
                    "model_cls": ProjectPlan,
                    "existing_query_cls": ProjectPlan,
                    "creation_func": create_project_plan,
                    "model_name": "Project Plan"
                })

        if data.projectMemberInfo and data.projectMemberInfo.project_member:
            project_members = data.projectMemberInfo.project_member

            for member in project_members:
                data_sections.append({
                    "data_dict": member.model_dump(),
                    "model_cls": ProjectMember,
                    "existing_query_cls": ProjectMember,
                    "creation_func": create_project_member,
                    "model_name": "Project Member"
                })

        responses = process_all_sections(db, project_id, data_sections)
        responses["Project Details"] = {"status": "success", "data": created_project.__dict__}

        return responses

    except Exception as e:
        db.rollback()
        print(f"Error in submit_all_project_data: {str(e)}")  # Log the error
        return {"status": "error", "error": f"Unexpected error: {str(e)}"}

def get_project_dashboard(db: Session=Depends(get_session)):
    projects = (
        db.query(
            ProjectDetails.project_name,
            ProjectDetails.project_code,
            ProjectDetails.color_mark,
            ProjectDetails.project_id,
        )
        .order_by(ProjectDetails.project_code)
        .all()
    )
    return [
        ProjectDashboardinfo(
            project_name = project.project_name,
            project_code = project.project_code,
            color_mark = project.color_mark,
            project_id = project.project_id
        )
        for project in projects
    ]

def get_project_details_by_id(db: Session, project_id: int) -> ProjectAllDetails:
    project = (
        db.query(ProjectDetails)
        .options(
            joinedload(ProjectDetails.project_duration),
            joinedload(ProjectDetails.project_bill),
            joinedload(ProjectDetails.project_plan),
            joinedload(ProjectDetails.project_members),
        )
        .filter(ProjectDetails.project_id == project_id)
        .first()
    )

    if not project: 
        raise HTTPException(status_code=404, detail=f"Project with project_id '{project_id}' not found.")
    
    return ProjectAllDetails(
        project_id=project.project_id,
        project_details= ProjectDetailsBase(**project.__dict__) if project else None,
        project_duration=ProjectDurationBase(**project.project_duration.__dict__) if project.project_duration else None,
        project_bills=ProjectBillBase(**project.project_bill.__dict__) if project.project_plan else None,
        project_plan=[ProjectPlanBase(**plan.__dict__) for plan in project.project_plan] if project.project_plan else [],
        project_member=[ProjectMemberBase(**member.__dict__) for member in project.project_members] if project.project_members else [],
    )

def fetch_managers(db: Session = Depends(get_session)):
    managers = (
        db.query(
            Users.emp_id,
            PersonalInfo.thai_name.label("name"),  # Fetch English name instead
            HiringInfo.position.label("position_id"),
            Position.position.label("position_name"),
        )
        .join(HiringInfo, Users.emp_id == HiringInfo.emp_id)
        .join(Position, HiringInfo.position == Position.id)
        .join(PersonalInfo, Users.emp_id == PersonalInfo.emp_id)  # Correct join
        .filter(Position.id == 10)  # Fetch only employees with position_id 10 (Manager)
        .all()
    )

    return [
        {
            "emp_id": manager.emp_id,
            "name": manager.name,  
            "position_id": manager.position_id,
            "position_name": manager.position_name,
        }
        for manager in managers
    ]

def get_project_assigned(
        db: Session = Depends(get_session), 
        auth: str = Depends(JWTBearer()),
    ):
    
    emp_id = decode_jwt(auth).get("emp_id")
    if not emp_id: 
        raise HTTPException(status_code=401, detail=EMP_ID_NOT_EXIST)

    projects = (
        db.query(ProjectDetails)
        .join(ProjectMember, ProjectDetails.project_id == ProjectMember.project_id) 
        .filter(ProjectMember.member_id == emp_id)  
        .options(joinedload(ProjectDetails.project_plan))  
        .order_by(ProjectDetails.project_code)
        .all()
    )

    return [
        ProjectAssigned(
            project_name=project.project_name,
            project_code=project.project_code,
            color_mark=project.color_mark,
            project_id=project.project_id,
            project_plan=[
                {
                    "id": plan.id,
                    "period_no": plan.period_no,
                    "deli_duration": plan.deli_duration,
                    "deli_date": plan.deli_date,
                    "deli_details": plan.deli_details,
                }
                for plan in project.project_plan 
            ],
        )
        for project in projects
    ]
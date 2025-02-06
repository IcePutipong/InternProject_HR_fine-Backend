from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class CreateProjectDetails(BaseModel):
    project_type: int
    project_code: str
    project_name: str
    project_contract_no: str
    project_details: Optional[str]= None
    project_client: int
    project_manager: int
    color_mark: str

class CreateProjectDuration(BaseModel):
    project_duration: int
    project_sign_date: date
    project_end_date: date
    number_of_periods: int

class CreateProjecBill(BaseModel):
    billable: bool
    project_value: float
    project_billing_rate: float

class SubmitProjectInfo(BaseModel):
    project_details: CreateProjectDetails
    project_duration: CreateProjectDuration
    project_bill: CreateProjecBill

class CreateProjectPlan(BaseModel):
    period_no: int
    deli_duration: date
    deli_date: date
    deli_details: Optional[str] = None

class SubmitProjectPlan(BaseModel):
    project_plan: List[CreateProjectPlan]

class CreateProjectMember(BaseModel):
    member_id: int
    position_id: int
    assigned_date: date
    assigned_detail: str

class SubmitProjectMember(BaseModel):
    project_member: List[CreateProjectMember]

class SubmitallProjectData(BaseModel):
    projectInfo: SubmitProjectInfo
    projectPlanInfo: SubmitProjectPlan
    projectMemberInfo: SubmitProjectMember

class GenerateProjectCode(BaseModel):
    project_type: int
    client_name: str

class GenerateProjectCodeRes(BaseModel):
    project_code: str

    model_config = {
        "from_attributes": True
    }


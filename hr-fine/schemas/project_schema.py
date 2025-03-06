from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class ProjectDetailsBase(BaseModel):
    project_type: int
    project_code: str
    project_name: str
    project_contract_no: str
    project_details: Optional[str]= None
    project_client: int
    project_manager: str
    color_mark: str

class ProjectDurationBase(BaseModel):
    project_duration: int
    project_sign_date: date
    project_end_date: date
    number_of_periods: int

class ProjectBillBase(BaseModel):
    billable: bool
    project_value: float
    project_billing_rate: float

class SubmitProjectInfo(BaseModel):
    project_details: ProjectDetailsBase
    project_duration: ProjectDurationBase
    project_bill: ProjectBillBase

class ProjectPlanBase(BaseModel):
    period_no: int
    deli_duration: int
    deli_date: date
    deli_details: Optional[str] = None

class SubmitProjectPlan(BaseModel):
    project_plan: List[ProjectPlanBase]

class ProjectMemberBase(BaseModel):
    member_id: str
    assigned_detail: str

class FetchProjectMember(BaseModel):
    project_member_id: int
    member_id: str
    assigned_detail: str

class SubmitProjectMember(BaseModel):
    project_member: List[ProjectMemberBase]

class SubmitallProjectData(BaseModel):
    projectInfo: SubmitProjectInfo
    projectPlanInfo: SubmitProjectPlan
    projectMemberInfo: SubmitProjectMember

class GenerateProjectCode(BaseModel):
    project_type: int
    client_id: int

class GenerateProjectCodeRes(BaseModel):
    project_code: str

    model_config = {
        "from_attributes": True
    }

class ProjectDashboardinfo (BaseModel):
    project_name: str
    project_code: str
    color_mark: str
    project_id: int

    model_config = {
        "from_attributes": True
    }

class FetchProjectPlan (BaseModel):
    id: int
    period_no: int
    deli_details: Optional[str] = None

class ProjectAssigned (BaseModel):
    project_name: str
    project_code: str
    color_mark: str
    project_id: int
    project_plan: List[FetchProjectPlan]

    model_config = {
        "from_attributes": True
    }

class ProjectAllDetails(BaseModel):
    project_id : int
    project_details: ProjectDetailsBase
    project_duration: ProjectDurationBase
    project_bills: ProjectBillBase
    project_plan: List[ProjectPlanBase]
    project_member: List[FetchProjectMember]

    model_config = {
        "from_attributes": True
    }

class ProjectDetailEdit(BaseModel):
    project_details: ProjectDetailsBase
    project_bills: ProjectBillBase

class ProjectDurationEdit(BaseModel):
    project_durations: ProjectDurationBase

class PlanEdit(BaseModel):
    project_plans: ProjectPlanBase

class ProjectMemberEdit(BaseModel):
    project_member: ProjectMemberBase

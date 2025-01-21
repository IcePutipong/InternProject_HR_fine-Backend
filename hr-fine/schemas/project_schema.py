from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class CreateProjectDetails(BaseModel):
    project_type: str
    project_code: str
    project_name: str
    project_contract_no: str
    project_details: Optional[str]= None
    project_client: str
    proejct_manager: str
    color_mark: str

class CreateProjectDuration(BaseModel):
    project_id: int
    project_duration: int
    project_sign_date: date
    project_end_date: date

class CreateProjecBill(BaseModel):
    project_id: int
    billable: bool
    project_value: float
    project_billing_rate: float

class CreateProject(BaseModel):
    project_details: CreateProjectDetails
    project_duration: CreateProjectDuration
    project_bill: CreateProjecBill

class CreateProjectPlan(BaseModel):
    project_id: int
    period_no: int
    deli_duration: date
    deli_date: date
    deli_details: str

class EditProjectDetails(BaseModel):
    project_code: Optional[str]= None
    project_name: Optional[str]= None
    project_contract_no: Optional[str]= None
    project_details: Optional[str]= None
    project_client: Optional[str]= None
    proejct_manager: Optional[str]= None
    color_mark: Optional[str]= None

class EditProjectDuration(BaseModel):
    project_id: Optional[int]= None
    project_duration: Optional[int]= None
    project_sign_date: Optional[date]= None
    project_end_date: Optional[date]= None

class EditProjectBill(BaseModel):
    project_id: Optional[int] = None
    billable: Optional[bool] = None
    project_value: Optional[float] = None
    project_billing_rate: Optional[float] = None

class EditProjectPlan(BaseModel):
    project_id: Optional[int] = None
    period_no: Optional[int] = None
    deli_duration: Optional[date] = None
    deli_date: Optional[date] = None
    deli_details: Optional[str] = None

class FetchProjectDetails(BaseModel):
    project_code: Optional[str]= None
    project_name: Optional[str]= None
    project_contract_no: Optional[str]= None
    project_details: Optional[str]= None
    project_client: Optional[str]= None
    proejct_manager: Optional[str]= None
    color_mark: Optional[str]= None

    model_config = {
        "from_attributes": True
    }

class FetchProjectDuration(BaseModel):
    project_id: Optional[int]= None
    project_duration: Optional[int]= None
    project_sign_date: Optional[date]= None
    project_end_date: Optional[date]= None

    model_config = {
        "from_attributes": True
    }

class FetchProjectBill(BaseModel):
    project_id: Optional[int] = None
    billable: Optional[bool] = None
    project_value: Optional[float] = None
    project_billing_rate: Optional[float] = None

    model_config = {
        "from_attributes": True
    }

class FetchProjectPlan(BaseModel):
    project_id: Optional[int] = None
    period_no: Optional[int] = None
    deli_duration: Optional[date] = None
    deli_date: Optional[date] = None
    deli_details: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class GenerateProjectCode(BaseModel):
    project_type: str
    client_name: str

class GenerateProjectCodeRes(BaseModel):
    project_code: str

    model_config = {
        "from_attributes": True
    }
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional


class AddCompany(BaseModel):
    company: str

class FetchCompany(BaseModel):
    id: int
    company: Optional[str] 

    model_config = {
        "from_attributes": True
    }

class AddEmployeeType(BaseModel):
    employee_type: str

class FetchEmployeeType(BaseModel):
    id: int
    employee_type: Optional[str] 

    model_config = {
        "from_attributes": True
    }

class AddContractType(BaseModel):
    contract_type: str

class FetchContractType(BaseModel):
    id: int
    contract_type: Optional[str]

    model_config = {
        "from_attributes": True
    }

class AddWorkingStatus(BaseModel):
    working_status: str

class FetchWorkingStatus(BaseModel):
    id: int
    working_status: str

    model_config = {
        "from_attributes": True
    }

class AddDepartment(BaseModel):
    department: str

class AddPosition (BaseModel):
    position: str
    department_id: int

class FetchPosition(BaseModel):
    id: int
    position: str
    department_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class FetchDepartment(BaseModel):
    id: int
    department: str
    positions: List[FetchPosition]

    model_config = {
        "from_attributes": True
    }

class EditPosition(BaseModel):
    id: int
    position: str
    department_id: int

class AddProjectType(BaseModel):
    project_types: str
    project_type_code: str

class ResProjectType(BaseModel):
    id: int 
    project_types: str

    model_config = {
        "from_attributes": True
    }



from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class CreateClient(BaseModel):
    client_name: str
    client_code: str
    client_type: int
    client_email: EmailStr
    contact_address: str
    client_tel: str

class EditClient(BaseModel):
    client_id: Optional[int] =None
    client_type: Optional[str] =None
    client_name: Optional[str] =None
    client_code: Optional[str] =None
    client_email: Optional[EmailStr] =None
    contact_address: Optional[str] =None
    client_tel: Optional[str] =None

class ClientRes(BaseModel):
    client_type: Optional[str] =None
    client_name: Optional[str] =None
    client_code: Optional[str] =None
    client_email: Optional[EmailStr] =None
    contact_address: Optional[str] =None
    client_tel: Optional[str] =None

    model_config = {
        "from_attributes": True
    }

class GenerateClientCode(BaseModel):
    client_name: str
    client_type: str
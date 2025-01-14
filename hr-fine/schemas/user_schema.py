from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class BaseUserSchema(BaseModel):
    emp_id:str

class CreatePersonalInfo(BaseUserSchema):
    nation_id: str = Field(..., pattern=r"^\d+$")
    exp_card_date: str
    thai_name: str
    eng_name: str
    thai_nickname: str
    eng_nickname: str
    gender: str
    nation: str
    religion: Optional[str] = None
    date_birth: Optional[date] = None

class CreateContactInfo(BaseUserSchema):
    personal_email: Optional[EmailStr] = None
    line_id: str

class CreateAddressInfo(BaseUserSchema):
    house_no: str
    village_no: int
    sub_district: str
    district: str
    province: str
    zipcode: str
    country: str
    room_no: Optional[str] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None

class CreateRegisAddressInfo(BaseUserSchema):
    house_no: str
    village_no: int
    sub_district: str
    district: str
    province: str
    zipcode: str
    country: str
    room_no: Optional[str] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None

class CreateUserInfoData(BaseModel):
    personal_info: CreatePersonalInfo
    contact_info: CreateContactInfo
    address_info: CreateAddressInfo
    regis_address_info: CreateRegisAddressInfo

class CreateHiringInfo(BaseUserSchema):
    start_date: date
    working_status: str
    prodation_date: date
    terminate_date: date
    working_location: str
    contract_type: str
    emp_type: str   
    department: str
    position: str
    manager: Optional[str] = None

class CreatePaymentinfo(BaseUserSchema):
    payment_type: str
    account_no: str
    bank: Optional[str] = None
    account_name: Optional[str] = None

class CreateDeductionInfo(BaseModel):
    deduct_social_security: bool
    social_security_company: Optional[str] = None
    social_security_emp_percentage: Optional[float] = None
    social_security_company_percentage: Optional[float] = None
    enroll_date: Optional[date] = None
    pri_healthcare: Optional[str] = None
    sec_healthcare: Optional[str] = None
    provide_fund_percentage: Optional[float] = None
    fee: Optional[float] = None

    has_social_security: bool
    establishment_location: Optional[str]
    deduct_SLF_IC: Optional[bool]
    pay_SLF_IC: Optional[float]

    has_other_details: bool
    other_details: Optional[str]
    other_expenses: Optional[float]
    other_percentage: Optional[float]

class CreateUserPayment(BaseModel):
    deduction_info: CreateDeductionInfo
    payment_info: CreatePaymentinfo

class SubmitInfoForm(BaseModel):
    user_info: CreateUserInfoData
    hiring_info: CreateHiringInfo
    payment_info: CreatePaymentinfo 

class EditPersonalInfo(BaseUserSchema):
    nation_id: Optional[str] = None
    exp_card_date: Optional[str] = None
    thai_name: Optional[str] = None
    eng_name: Optional[str] = None
    thai_nickname: Optional[str] = None
    eng_nickname: Optional[str] = None
    gender: Optional[str] = None
    nation: Optional[str] = None
    religion: Optional[str] = None
    date_birth: Optional[date] = None

class EditContactInfo(BaseUserSchema):
    personal_email: Optional[EmailStr] = None
    line_id: Optional[str] = None

class EditAddressInfo(BaseUserSchema):
    house_no: Optional[str] = None
    village_no: Optional[int] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None
    room_no: Optional[str] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None

class EditRegisAddressInfo(BaseUserSchema):
    house_no: Optional[str] = None
    village_no: Optional[int] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None
    room_no: Optional[str] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley:Optional[str] = None
    road: Optional[str] = None

class EditUserInfoData(BaseUserSchema):
    edit_personal_info: Optional[EditPersonalInfo] = None
    edit_contact_info: Optional[EditContactInfo] = None
    edit_address_info: Optional[EditAddressInfo] = None
    edit_regis_address_info: Optional[EditRegisAddressInfo] = None

class EditHiringInfo(BaseUserSchema):
    start_date: Optional[date] = None
    working_status: Optional[bool] = None
    prodation_date: Optional[date] = None
    terminate_date: Optional[date] = None
    working_location: Optional[str] = None
    contract_type: Optional[str] = None
    agency: Optional[str] = None
    position: Optional[str] = None
    manager: Optional[str] = None

class EditPaymentinfo(BaseUserSchema):
    payment_period: Optional[date] = None
    payment_type: Optional[str] = None
    account_no: Optional[str] = None
    bank: Optional[str] = None
    account_name: Optional[str] = None

class PersonalInfoRes(BaseModel):
    nation_id: Optional[str]
    exp_card_date: Optional[str]
    thai_name: Optional[str]
    eng_name: Optional[str]
    thai_nickname: Optional[str]
    eng_nickname: Optional[str]
    gender: Optional[str]
    nation: Optional[str]
    religion: Optional[str]
    date_birth: Optional[date]

    model_config = {
        "from_attributes": True
    }

class AddressInfoRes(BaseModel):
    house_no: Optional[str]
    village_no: Optional[int]
    sub_district: Optional[str]
    district: Optional[str]
    province: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    room_no: Optional[str]
    floor: Optional[int]
    village: Optional[str]
    building: Optional[str]
    alley: Optional[str]
    road: Optional[str]

    model_config = {
        "from_attributes": True
    }

class RegAddressInfoRes(BaseModel):
    house_no: Optional[str]
    village_no: Optional[int]
    sub_district: Optional[str]
    district: Optional[str]
    province: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    room_no: Optional[str]
    floor: Optional[int]
    village: Optional[str]
    building: Optional[str]
    alley: Optional[str]
    road: Optional[str]

    model_config = {
        "from_attributes": True
    }

class ContactInfoRes(BaseModel):
    company_email: Optional[EmailStr]
    personal_email: Optional[EmailStr]
    line_id: Optional[str]

    model_config = {
        "from_attributes": True
    }

class UserInfoRes(BaseModel):
    emp_id: str
    email: EmailStr
    personal_info: Optional[PersonalInfoRes]
    address_info: List[AddressInfoRes]
    regis_address: List[AddressInfoRes]
    contact_info: Optional[ContactInfoRes]

    model_config = {
        "from_attributes": True
    }

class PaymentInfoRes(BaseModel):
    payment_period: Optional[date]
    payment_type: Optional[str]
    account_no: Optional[str]
    bank: Optional[str]
    account_name: Optional[str]

    model_config = {
        "from_attributes": True
    }

class HiringInfoRes(BaseModel):
    emp_id: str
    start_date: Optional[date]
    working_status: Optional[bool]
    prodation_date: Optional[date] = None
    terminate_date: Optional[date] = None
    working_location: Optional[str]
    contract_type: Optional[str]
    agency: Optional[str] = None
    position: Optional[str]
    manager: Optional[str] = None

    model_config = {
        "from_attributes": True
    }








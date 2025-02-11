from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonalInfoBase(BaseModel):
    nation_id: str
    thai_name: str
    eng_name: str
    thai_nickname: str
    eng_nickname: str
    gender: str
    nation: str
    religion: Optional[str] = None
    date_birth: Optional[str] = None


class AddressInfoBase(BaseModel):
    house_no: str
    village_no: int
    sub_district: str
    district: str
    province: str
    zipcode: str
    country: str
    room_no: Optional[int] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None


class RegistrationAddressBase(BaseModel):
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

    
class ContactInfoBase(BaseModel):
    tel: str
    line_id: str


class SubmitUserInfo(BaseModel):
    personal_info: PersonalInfoBase
    address_info: AddressInfoBase
    registration_address: RegistrationAddressBase
    contact_info: ContactInfoBase

class HiringInfoBase(BaseModel):
    start_date: date
    working_status: str
    prodation_date: date
    terminate_date: date
    emp_type: str
    working_location: str
    contract_type: str
    department: int 
    position: int
    manager: str


class SubmitHiringInfo(BaseModel):
    hiring_info: HiringInfoBase

class PaymentInfoBase(BaseModel):
    payment_type: str
    account_no: Optional[str] = None
    bank: Optional[str] = None
    account_name: Optional[str] = None


class DeductionInfoBase(BaseModel):
    deduct_social_security: bool = False
    social_security_company: Optional[str] = None
    social_security_emp_percentage: Optional[float] = None
    social_security_company_percentage: Optional[float] = None
    enroll_date: Optional[str] = None
    pri_healthcare: Optional[str] = None
    sec_healthcare: Optional[str] = None
    provide_fund_percentage: Optional[float] = None
    fee: Optional[float] = None

    has_social_security: bool = False
    establishment_location: Optional[str] = None

    deduct_SLF_IC: bool = False
    pay_SLF_IC: Optional[float] = None


class SubmitPaymentInfo(BaseModel):
    payment_info: PaymentInfoBase
    deduction_info: Optional[DeductionInfoBase] = None


class SubmitAllInfoData(BaseModel):
    emp_id: str
    userInfo: SubmitUserInfo
    hiringInfo: SubmitHiringInfo
    paymentInfo: SubmitPaymentInfo

class EmployeeDashboardInfo(BaseModel):
    emp_id: str
    id: int
    thai_name: str
    position: str
    working_location: str
    email: str

    class Config:
        from_attributes = True

class EmployeeDetails(BaseModel):
    emp_id: str
    email: str
    personal_info: Optional[PersonalInfoBase] = None
    address_info: Optional[AddressInfoBase] = None
    registration_address: Optional[RegistrationAddressBase] = None
    contact_info: Optional[ContactInfoBase] = None
    hiring_info: Optional[HiringInfoBase] = None
    payment_info: Optional[PaymentInfoBase] = None
    deduction_info: Optional[DeductionInfoBase] = None

    class Config:
        from_attributes = True

class UpdatePersonalInfo(BaseModel):
    nation_id: Optional[str] = None
    thai_name: Optional[str] = None
    eng_name: Optional[str] = None
    thai_nickname: Optional[str] = None
    eng_nickname: Optional[str] = None
    gender: Optional[str] = None
    nation: Optional[str] = None
    religion: Optional[str] = None
    date_birth: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateAddressInfo(BaseModel):
    house_no: Optional[str] = None
    village_no: Optional[int] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None
    room_no: Optional[int] = None
    floor: Optional[int] = None
    village: Optional[str] = None
    building: Optional[str] = None
    alley: Optional[str] = None
    road: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateRegistrationAddress(BaseModel):
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

    class Config:
        from_attributes = True

class UpdateContactInfo(BaseModel):
    email: Optional[EmailStr] = None  #
    tel: Optional[str] = None
    line_id: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateHiringInfo(BaseModel):
    start_date: Optional[date] = None
    working_status: Optional[str] = None
    prodation_date: Optional[date] = None
    terminate_date: Optional[date] = None
    emp_type: Optional[str] = None
    working_location: Optional[str] = None
    contract_type: Optional[str] = None
    department: Optional[int] = None
    position: Optional[int] = None
    manager: Optional[str] = None

    class Config:
        from_attributes = True

class UpdatePaymentInfo(BaseModel):
    payment_type: Optional[str] = None
    account_no: Optional[str] = None
    bank: Optional[str] = None
    account_name: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateDeductionInfo(BaseModel):
    deduct_social_security: Optional[bool] = None
    social_security_company: Optional[str] = None
    social_security_emp_percentage: Optional[float] = None
    social_security_company_percentage: Optional[float] = None
    enroll_date: Optional[str] = None
    pri_healthcare: Optional[str] = None
    sec_healthcare: Optional[str] = None
    provide_fund_percentage: Optional[float] = None
    fee: Optional[float] = None
    has_social_security: Optional[bool] = None
    establishment_location: Optional[str] = None
    deduct_SLF_IC: Optional[bool] = None
    pay_SLF_IC: Optional[float] = None

    class Config:
        from_attributes = True
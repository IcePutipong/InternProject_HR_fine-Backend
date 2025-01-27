from datetime import date
from pydantic import BaseModel
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
    address_info: Optional[AddressInfoBase] = None
    registration_address: Optional[RegistrationAddressBase] = None
    contact_info: Optional[ContactInfoBase] = None

class HiringInfoBase(BaseModel):
    start_date: date
    working_status: str
    prodation_date: date
    terminate_date: date
    emp_type: str
    working_location: str
    contract_type: str
    department: str
    position: str
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
from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from models.user_model import Company, ContractType, DeductionInfo, Department, EmployeeType, Position, PersonalInfo, AddressInfo, RegistrationAddress, PaymentInfo, HiringInfo, ContactInfo, WorkingStatus
from schemas.user_schema import AddressInfoRes, ContactInfoRes, CreateUserInfoData, CreatePaymentinfo, CreateHiringInfo, CreateUserPayment, EditHiringInfo, EditPaymentinfo, EditUserInfoData, HiringInfoRes, PaymentInfoRes, PersonalInfoRes, RegAddressInfoRes, SubmitInfoForm, UserInfoRes
from schemas.optional_schema import FetchPosition, FetchCompany, FetchContractType, FetchDepartment, FetchEmployeeType, FetchWorkingStatus
from sqlalchemy.orm import Session, joinedload
from constants import ID_NOT_FOUND
from models.auth_model import Users


def update_model_data(model, data: Dict):
    for key, value in data.items():
        setattr(model, key, value)

def create_user_info(request: CreateUserInfoData, db: Session=Depends(get_session)):
    user = db.query(Users).filter(Users.emp_id == request.personal_info.emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found, can't create user info.")
    
    emp_id = user.emp_id

    new_personal_info = PersonalInfo(
        emp_id=emp_id,
        nation_id=request.personal_info.nation_id,
        exp_card_date=request.personal_info.exp_card_date,
        thai_name=request.personal_info.thai_name,
        eng_name=request.personal_info.eng_name,
        thai_nickname=request.personal_info.thai_nickname,
        eng_nickname=request.personal_info.eng_nickname,
        gender=request.personal_info.gender,
        nation=request.personal_info.nation,
        religion=request.personal_info.religion,
        date_birth=request.personal_info.date_birth,    
    )
    db.add(new_personal_info)

    new_address_info = AddressInfo(
        emp_id=emp_id,
        house_no=request.address_info.house_no,
        village_no=request.address_info.village_no,
        sub_district=request.address_info.sub_district,
        district=request.address_info.district,
        province=request.address_info.province,
        zipcode=request.address_info.zipcode,
        country=request.address_info.country,
        room_no=request.address_info.room_no,
        floor=request.address_info.floor,
        village=request.address_info.village,
        building=request.address_info.building,
        alley=request.address_info.alley,
        road=request.address_info.road,
    )
    db.add(new_address_info)

    new_regis_address_info = RegistrationAddress(
        emp_id=emp_id,
        house_no=request.address_info.house_no,
        village_no=request.address_info.village_no,
        sub_district=request.address_info.sub_district,
        district=request.address_info.district,
        province=request.address_info.province,
        zipcode=request.address_info.zipcode,
        country=request.address_info.country,
        room_no=request.address_info.room_no,
        floor=request.address_info.floor,
        village=request.address_info.village,
        building=request.address_info.building,
        alley=request.address_info.alley,
        road=request.address_info.road,
    )
    db.add(new_regis_address_info)

    new_contact_info = ContactInfo(
        emp_id=emp_id,
        email=request.contact_info.email,
        tel =request.contact_info.tel,
        line_id=request.contact_info.line_id
    )
    db.add(new_contact_info)

    db.commit()
    db.refresh(new_personal_info)
    db.refresh(new_address_info)
    db.refresh(new_regis_address_info)
    db.refresh(new_contact_info)
    return{
        "personal_info": new_personal_info,
        "address_info": new_address_info,
        "regis_address_info": new_regis_address_info,
        "contact_info": new_contact_info
    }

def edit_user_info(request: EditUserInfoData, db: Session = Depends(get_session)) -> Dict[str, Any]:
    user = db.query(Users).filter(Users.emp_id == request.emp_id).first()
    if not user: 
        raise HTTPException(status_code=404, detail="User with ID does not exist.")
    
    model_mapping = [
        (request.edit_personal_info, PersonalInfo),
        (request.edit_address_info, AddressInfo),
        (request.edit_regis_address_info, RegistrationAddress),
        (request.edit_contact_info, ContactInfo),
    ]

    for schema, model_class in model_mapping:
        if schema:
            model_instance = db.query(model_class).filter(model_class.emp_id == user.emp_id).first()
            if model_instance:
                update_model_data(model_instance, schema.model_dump(exclude_unset=True))

    db.commit()
    return{
        "message": "User Info updated successfully.",
        "emp_id": user.emp_id,
    }

def get_user_info(emp_id: str, db: Session=Depends(get_session)) -> UserInfoRes:
    user = (
        db.query(Users).filter(Users.emp_id == emp_id)
        .options(
            joinedload(Users.personal_info),
            joinedload(Users.address_info),
            joinedload(Users.registration_address),
            joinedload(Users.contact_info),
        )
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail=ID_NOT_FOUND)

    personal_info = (
        PersonalInfoRes.model_validate(user.personal_info[0]) if user.personal_info else None
    )
    address_info = [
        AddressInfoRes.model_validate(addr) for addr in user.address_info
    ] if user.address_info else []
    regis_address = [
        RegAddressInfoRes.model_validate(addr) for addr in user.registration_address
    ] if user.registration_address else []
    contact_info = (
        ContactInfoRes.model_validate(user.contact_info[0]) if user.contact_info else None
    )
    return UserInfoRes(        
        emp_id=user.emp_id,
        email=user.email,
        personal_info=personal_info,
        address_info=address_info,
        regis_address=regis_address,
        contact_info=contact_info,
        )

def create_hiring_info(request: CreateHiringInfo, db: Session=Depends(get_session)):
    user = db.query(Users).filter(Users.emp_id == request.emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found, can't create hiring info.")
    
    emp_id = user.emp_id

    new_hiring_info = HiringInfo(
        emp_id=emp_id,
        start_date=request.start_date,
        working_status=request.working_status,
        prodation_date=request.prodation_date,
        terminate_date=request.terminate_date,
        working_location=request.working_location,
        contract_type=request.contract_type,
        department=request.department,
        position=request.position,
        manager=request.manager,
        emp_type=request.emp_type,
    )
    db.add(new_hiring_info)

    db.commit()
    db.refresh(new_hiring_info)
    return{
        "hiring_info": new_hiring_info
    }


def edit_hiring_info(request: EditHiringInfo, db: Session = Depends(get_session)):
    user = db.query(Users).filter(Users.emp_id == request.emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=ID_NOT_FOUND)
    
    hiring_info = db.query(HiringInfo).filter(HiringInfo.emp_id == user.emp_id).first()
    
    update_model_data(hiring_info, request.model_dump(exclude_unset=True))

    db.commit()
    db.refresh(hiring_info)

    return {
        "message": "Hiring Information updated successfully.",
        "hiring_info": hiring_info
    }

def get_hiring_info(emp_id: str, db: Session = Depends(get_session)) -> HiringInfoRes:
    user = db.query(Users).filter(Users.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=ID_NOT_FOUND)
    
    hiring_info = db.query(HiringInfo).filter(HiringInfo.emp_id == emp_id).first()
    if not hiring_info:
        raise HTTPException(status_code=404, detail="Hiring Information not found for this User.")
    
    return HiringInfoRes.model_validate(hiring_info)


def create_user_payment_info(request: CreateUserPayment, db: Session=Depends(get_session)):
    user = db.query(Users).filter(Users.emp_id == request.payment_info.emp_id).first()
    if not user: 
        raise HTTPException(status_code=404, detail="User not found, can't create user info.")
    
    emp_id = user.emp_id

    new_payment_info = PaymentInfo(
        emp_id=emp_id,
        payment_type=request.payment_type,
        account_no=request.account_no,
        bank=request.bank,
        account_name=request.account_name
    )
    db.add(new_payment_info)

    new_deduction_info = DeductionInfo(
        emp_id=emp_id,
        deduct_social_security=request.deduct_social_security,
        social_security_company=request.social_security_company,
        social_security_emp_percentage=request.social_security_emp_percentage,
        social_security_company_percentage=request.social_security_company_percentage,
        enroll_date=request.enroll_date,
        pri_healthcare=request.pri_healthcare,
        sec_healthcare=request.sec_healthcare,
        provide_fund_percentage=request.provide_fund_percentage,
        fee=request.fee,
        
        has_social_security=request.has_social_security,
        establishment_location=request.establishment_location,
        deduct_SLF_IC=request.deduct_SLF_IC,
        pay_SLF_IC=request.pay_SLF_IC,

        has_other_details=request.has_other_details,
        other_details=request.other_details,
        other_expenses=request.other_expenses,
        other_percentage=request.other_percentage,
    )
    db.add(new_deduction_info)
    db.commit()
    db.refresh(new_payment_info)
    db.refresh(new_deduction_info)

    return{
        "payment_info": new_payment_info,
        "deduction_info": new_deduction_info,
    }

# def create_payment_info(request:CreatePaymentinfo, db: Session=Depends(get_session)):
#     user = db.query(Users).filter(Users.emp_id == request.emp_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found, can't create payment info.")
    
#     emp_id = user.emp_id

#     new_payment_info = PaymentInfo(
#         emp_id=emp_id,
#         payment_period=request.payment_period,
#         payment_type=request.payment_type,
#         account_no=request.account_no,
#         bank=request.bank,
#         account_name=request.account_name
#     )
#     db.add(new_payment_info)

#     db.commit()
#     db.refresh(new_payment_info)
#     return{
#         "payment_info": new_payment_info
#     }

# def edit_payment_info(request: EditPaymentinfo, db: Session = Depends(get_session)):
#     user = db.query(Users). filter(Users.emp_id == request.emp_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail=ID_NOT_FOUND)

#     payment_info = db.query(PaymentInfo).filter(PaymentInfo.emp_id == user.emp_id).first()
    
#     update_model_data(payment_info, request.model_dump(exclude_unset=True))

#     db.commit()
#     db.refresh(payment_info)

#     return {
#         "message": "Payment Information updated successfully.",
#         "payment_info": payment_info
#     }

# def get_payment_info(emp_id: str, db: Session = Depends(get_session)) -> PaymentInfoRes:
#     user = db.query(Users).filter(Users.emp_id == emp_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail=ID_NOT_FOUND)
    
#     payment_info = db.query(PaymentInfo).filter(PaymentInfo.emp_id == emp_id).first()
#     if not payment_info:
#         raise  HTTPException(status_code=404, detail="Payment Information not found for this User.")
    
#     return PaymentInfoRes.model_validate(payment_info)

def submit_all_user_info(request: SubmitInfoForm, db: Session = Depends(get_session)):
    try:
        with db.begin():
            user =db.query(Users).filter(Users.emp_id == request.emp_id).first()
            if not user: 
                raise HTTPException(status_code=404, detail="User not found, can't create hiring info.")

            create_user_info(request.user_info.personal_info, db)
            create_user_info(request.user_info.contact_info,db)
            create_user_info(request.user_info.address_info,db)
            create_user_info(request.user_info.regis_address_info,db)
            create_hiring_info(request.hiring_info,db)
            create_payment_info(request.payment_info,db)

            db.commit()

            return{"message": "The User data submited Successfully."}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to subbmit Data: {str(e)}")
    
def fetch_company(db: Session = Depends(get_session)):
    companies = db.query(Company).all()
    return[{"id": company.id, "company": company.company} for company in companies]

def fetch_emp_type(db: Session = Depends(get_session)):
    employee_types = db.query(EmployeeType).all()
    return [{"id": emp_type.id, "employee_type": emp_type.employee_type } for emp_type in employee_types]

def fetch_contract(db: Session = Depends(get_session)):
    contrac_types = db.query(ContractType).all()
    return [{"id": contract_type.id, "contract_type": contract_type.contract_type} for contract_type in contrac_types] 

def fetch_department(db: Session = Depends(get_session)):
    departments = db.query(Department).options(joinedload(Department.positions)).all()

    department_list = []
    for department in departments:
        position = [
            FetchPosition.model_validate(position)
            for position in department.positions if position.department_id is not None
        ]
        department_list.append(
            FetchDepartment(
                id = department.id,
                department = department.department,
                positions=position
            )
        )
    return department_list

def fetch_positions(db: Session = Depends(get_session)) -> List[FetchPosition]:
    positions = db.query(Position).all()
    return [FetchPosition.model_validate(position) for position in positions]

def fetch_working_status(db: Session = Depends(get_session)):
    worked_status = db.query(WorkingStatus).all()
    return [{"id": working_status.id, "working_status": working_status.working_status} for working_status in worked_status]




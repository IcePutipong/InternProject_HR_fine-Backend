from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from models.user_model import DeductionInfo, HiringInfo, PaymentInfo, PersonalInfo, AddressInfo, Position, RegistrationAddress, ContactInfo  
from schemas.user_schema import AddressInfoBase,ContactInfoBase, DeductionInfoBase, EmployeeDashboardInfo, EmployeeDetails, HiringInfoBase, PaymentInfoBase,PersonalInfoBase,RegistrationAddressBase, SubmitAllInfoData, SubmitHiringInfo, SubmitPaymentInfo, SubmitUserInfo
from sqlalchemy.orm import Session, joinedload
from constants import ID_NOT_FOUND
from models.auth_model import Users


def update_model_data(model, data: Dict):
    for key, value in data.items():
        setattr(model, key, value)


def create_personal_info(db: Session, emp_id: str, personal_info_data: dict):
    personal_info_data["emp_id"] = emp_id
    db_personal_info = PersonalInfo(**personal_info_data)  
    db.add(db_personal_info)
    db.commit()
    db.refresh(db_personal_info)
    return db_personal_info

def create_address_info(db: Session, emp_id: str, address_info_data: dict):
    address_info_data["emp_id"] = emp_id
    db_address_info = AddressInfo(**address_info_data) 
    db.add(db_address_info)
    db.commit()
    db.refresh(db_address_info)
    return db_address_info

def create_registration_address(db: Session, emp_id: str, reg_address_data: dict):
    reg_address_data["emp_id"] = emp_id
    db_registration_address = RegistrationAddress(**reg_address_data)  
    db.add(db_registration_address)
    db.commit()
    db.refresh(db_registration_address)
    return db_registration_address

def create_contact_info(db: Session, emp_id: str, contact_info_data: dict):
    user = db.query(Users).filter(Users.emp_id == emp_id).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User with emp_id '{emp_id}' does not exist."
        )

    contact_info_data["email"] = user.email
    contact_info_data["emp_id"] = emp_id

    db_contact_info = ContactInfo(**contact_info_data)
    db.add(db_contact_info)
    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info

def create_hiring_info(db: Session, emp_id: str, hiring_info_data: dict):
    hiring_info_data["emp_id"] = emp_id
    db_hiring_info = HiringInfo(**hiring_info_data)
    db.add(db_hiring_info)
    db.commit()
    db.refresh(db_hiring_info)
    return db_hiring_info
    
def create_payment_info(db: Session, emp_id: str, payment_info_data: dict):
    payment_info_data["emp_id"] = emp_id
    db_payment_info = PaymentInfo(**payment_info_data)
    db.add(db_payment_info)
    db.commit()
    db.refresh(db_payment_info)
    return db_payment_info

def create_deduction_info(db: Session, emp_id: str, deduction_info_data: dict):
    deduction_info_data["emp_id"] = emp_id
    db_deduction_info = DeductionInfo(**deduction_info_data)
    db.add(db_deduction_info)
    db.commit()
    db.refresh(db_deduction_info)
    return db_deduction_info

def process_model_creation(
    db: Session,
    emp_id: str,
    model_cls,
    existing_query_cls,
    creation_func,
    data_dict: dict,
    model_name: str,
):

    try:
        existing_data = db.query(existing_query_cls).filter(existing_query_cls.emp_id == emp_id).first()
        if existing_data:
            return {
                "status": "error",
                "error": f"{model_name} with emp_id '{emp_id}' already exists."
            }
        
        new_data = creation_func(db, emp_id, data_dict)
        return {
            "status": "success",
            "data": new_data
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "error": str(e)
        }
    
def process_all_sections(
    db: Session,
    emp_id: str,
    data_sections: List[Dict[str, Any]]
):

    responses = {}
    for section in data_sections:
        if section["data_dict"]:  # Process only if data exists
            responses[section["model_name"]] = process_model_creation(
                db=db,
                emp_id=emp_id,
                model_cls=section["model_cls"],
                existing_query_cls=section["existing_query_cls"],
                creation_func=section["creation_func"],
                data_dict=section["data_dict"],
                model_name=section["model_name"]
            )
    return responses

def submit_all_user_data(db: Session, data: SubmitAllInfoData) -> dict:
    emp_id = data.emp_id
    data_sections = []

    if data.userInfo:
        user_info = data.userInfo
        data_sections.extend([
            {
                "data_dict": user_info.personal_info.model_dump() if user_info.personal_info else None,
                "model_cls": PersonalInfo,
                "existing_query_cls": PersonalInfo,
                "creation_func": create_personal_info,
                "model_name": "Personal info"
            },
            {
                "data_dict": user_info.address_info.model_dump() if user_info.address_info else None,
                "model_cls": AddressInfo,
                "existing_query_cls": AddressInfo,
                "creation_func": create_address_info,
                "model_name": "Address info"
            },
            {
                "data_dict": user_info.registration_address.model_dump() if user_info.registration_address else None,
                "model_cls": RegistrationAddress,
                "existing_query_cls": RegistrationAddress,
                "creation_func": create_registration_address,
                "model_name": "Registration address"
            },
            {
                "data_dict": user_info.contact_info.model_dump() if user_info.contact_info else None,
                "model_cls": ContactInfo,
                "existing_query_cls": ContactInfo,
                "creation_func": create_contact_info,
                "model_name": "Contact info"
            }
        ])

    if data.hiringInfo:
        hiring_info = data.hiringInfo
        data_sections.append({
            "data_dict": hiring_info.hiring_info.model_dump() if hiring_info.hiring_info else None,
            "model_cls": HiringInfo,
            "existing_query_cls": HiringInfo,
            "creation_func": create_hiring_info,
            "model_name": "Hiring info"
        })

    if data.paymentInfo:
        payment_info = data.paymentInfo
        data_sections.extend([
            {
                "data_dict": payment_info.payment_info.model_dump() if payment_info.payment_info else None,
                "model_cls": PaymentInfo,
                "existing_query_cls": PaymentInfo,
                "creation_func": create_payment_info,
                "model_name": "Payment info"
            },
            {
                "data_dict": payment_info.deduction_info.model_dump() if payment_info.deduction_info else None,
                "model_cls": DeductionInfo,
                "existing_query_cls": DeductionInfo,
                "creation_func": create_deduction_info,
                "model_name": "Deduction info"
            }
        ])

    return process_all_sections(db, emp_id, data_sections)

def get_all_employees_dashboard(db: Session):
    employees = (
        db.query(
            Users.emp_id,
            PersonalInfo.thai_name,
            Position.position.label("position_name"),
            HiringInfo.working_location,
            Users.email
        )
        .outerjoin(PersonalInfo, Users.emp_id == PersonalInfo.emp_id)
        .outerjoin(HiringInfo, Users.emp_id == HiringInfo.emp_id)      
        .outerjoin(ContactInfo, Users.emp_id == ContactInfo.emp_id) 
        .outerjoin(Position, HiringInfo.position == Position.id)   
        .all()
    )

    return [
        EmployeeDashboardInfo(
            emp_id=emp.emp_id,
            thai_name=emp.thai_name or "N/A",  
            position=emp.position_name or "N/A",  
            working_location=emp.working_location or "N/A",  
            email=emp.email or "N/A"          
        )
        for emp in employees
    ]

def get_employee_details_by_id(db: Session, emp_id: str) -> EmployeeDetails:
    user = (
        db.query(Users)
        .options(
            joinedload(Users.personal_info),
            joinedload(Users.address_info),
            joinedload(Users.registration_address),
            joinedload(Users.contact_info),
            joinedload(Users.hiring_info),
            joinedload(Users.payment_info),
            joinedload(Users.deduction_info),
        )
        .filter(Users.emp_id == emp_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail=f"Employee with emp_id '{emp_id}' not found.")

    personal_info_data = user.personal_info.__dict__ if user.personal_info else None
    if personal_info_data and personal_info_data.get("date_birth"):
        personal_info_data["date_birth"] = personal_info_data["date_birth"].isoformat()

    deduction_info_data = user.deduction_info.__dict__ if user.deduction_info else None
    if deduction_info_data and deduction_info_data.get("enroll_date"):
        deduction_info_data["enroll_date"] = deduction_info_data["enroll_date"].isoformat()

    return EmployeeDetails(
        emp_id=user.emp_id,
        email=user.email,
        personal_info=PersonalInfoBase(**personal_info_data) if personal_info_data else None,
        address_info=AddressInfoBase(**user.address_info.__dict__) if user.address_info else None,
        registration_address=RegistrationAddressBase(**user.registration_address.__dict__) if user.registration_address else None,
        contact_info=ContactInfoBase(**user.contact_info.__dict__) if user.contact_info else None,
        hiring_info=HiringInfoBase(**user.hiring_info.__dict__) if user.hiring_info else None,
        payment_info=PaymentInfoBase(**user.payment_info.__dict__) if user.payment_info else None,
        deduction_info=DeductionInfoBase(**user.deduction_info.__dict__) if user.deduction_info else None,
    )

def update_or_create_employee_info(db: Session, emp_id: str, model, update_data: dict, create_if_not_exists=True):
    """ 
    Generic function to update any employee-related model.
    - If the record exists, it updates the existing data.
    - If the record does not exist and `create_if_not_exists=True`, it creates a new record.
    """
    record = db.query(model).filter(model.emp_id == emp_id).first()

    if not record:
        if create_if_not_exists:
            new_record = model(emp_id=emp_id, **update_data)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return new_record
        else:
            raise HTTPException(status_code=404, detail=f"Record for {model.__tablename__} with emp_id '{emp_id}' not found.")

    for key, value in update_data.items():
        if value is not None:
            setattr(record, key, value)
    
    db.commit()
    db.refresh(record)
    return record


def update_contact_info(db: Session, emp_id: str, contact_data: dict):
    """
    Special function to update ContactInfo and Users email together.
    Ensures that if the email is changed, it updates both the auth table (`Users`) and `ContactInfo`.
    """
    contact_info = db.query(ContactInfo).filter(ContactInfo.emp_id == emp_id).first()
    user = db.query(Users).filter(Users.emp_id == emp_id).first()

    if not contact_info or not user:
        raise HTTPException(status_code=404, detail=f"ContactInfo or User record not found for emp_id '{emp_id}'")

    if "email" in contact_data:
        user.email = contact_data["email"]  
        contact_info.email = contact_data["email"]  

    for key, value in contact_data.items():
        if value is not None:
            setattr(contact_info, key, value)

    db.commit()
    db.refresh(contact_info)
    db.refresh(user)
    return contact_info

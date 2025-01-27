from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from models.user_model import DeductionInfo, HiringInfo, PaymentInfo, PersonalInfo, AddressInfo, RegistrationAddress, ContactInfo  
from schemas.user_schema import AddressInfoBase,ContactInfoBase, HiringInfoBase,PersonalInfoBase,RegistrationAddressBase, SubmitAllInfoData, SubmitHiringInfo, SubmitPaymentInfo, SubmitUserInfo
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

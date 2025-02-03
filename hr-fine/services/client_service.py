from typing import Any, Dict, List
from fastapi import HTTPException, Depends
from database.db import get_session
from schemas.client_schema import ClientDashboardInfo, CreateClient, EditClient
from sqlalchemy.orm import Session, joinedload
from models.client_model import Client
from models.project_model import ProjectType
from services.user_service import update_model_data

def create_client_info(request: CreateClient, db: Session = Depends(get_session)):
    existing_client = db.query(Client).filter(Client.client_name == request.client_name).first()
    if existing_client:
        raise HTTPException(status_code=400, detail=f"Client with {request.client_name} Already Exist.")
    
    existing_client_code = db.query(Client).filter(Client.client_code == request.client_code).first()
    if existing_client_code:
        raise HTTPException(status_code=400, detail=f"Client code with {request.client_code} already exist pls try other code.")

    new_client_info = Client(
        client_type=request.client_type,
        client_name=request.client_name,
        client_code= request.client_code,
        client_email = request.client_email,
        contact_address = request.contact_address,
        client_tel = request.client_tel
    )
    db.add(new_client_info)
    db.commit()
    db.refresh(new_client_info)
    return {
        "client_type": new_client_info.client_type,
        "client_name":new_client_info.client_name,
        "client_code": new_client_info.client_code,
        "client_email": new_client_info.client_email,
        "contact_address": new_client_info.contact_address,
        "client_tel": new_client_info.client_tel,
    }

def  edit_client_info(request: EditClient, db: Session =Depends(get_session)):
    client = db.query(Client).filter(Client.client_id == request.client_id).first()
    if not client: 
        raise HTTPException(status_code=404, detail="Client not found in the database, Pls Check again.")
    
    client_info = db.query(Client).filter(Client.client_id == client.client_id).first()
    update_model_data(client_info, request.model_dump(exclude_unset=True))

    db.commit()
    db.refresh(client_info)

    return {
        "message": "Client Infomation update Successfully.",
        "client_info": client_info
    }

def get_client_dashboard(db: Session):
    clients = (
        db.query(
            Client.client_id,
            Client.client_code,
            Client.client_email,
            Client.client_name,
            ProjectType.project_types.label("project_type"),
            Client.contact_address,
            Client.client_tel
        )
        .join(ProjectType, Client.client_type == ProjectType.id)
        .all()
    )

    return [
        ClientDashboardInfo(
            client_id=client.client_id,
            client_code=client.client_code,
            client_name=client.client_name,
            client_type=client.project_type,
            client_email=client.client_email,
            contact_address=client.contact_address,
            client_tel=client.client_tel
        )
        for client in clients
    ]

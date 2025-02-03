from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, index=True)

    client_type = Column(Integer,ForeignKey("project_types.id") ,nullable=False)
    client_name =Column(String(50), nullable=False, unique=True)
    client_code = Column(String(10), nullable=False, unique=True)
    client_email = Column(String(30), nullable=False)
    contact_address = Column(String(1000), nullable=False)
    client_tel = Column(String(15), nullable=False)

    project_details = relationship("ProjectDetails", back_populates="client")
    types = relationship = relationship( "ProjectType", back_populates="client_type")


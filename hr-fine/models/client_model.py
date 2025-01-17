from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, index=True)

    client_type = Column(String(20), nullable=False)
    client_name =Column(String(20), nullable=False)
    client_code = Column(String(10), nullable=False)
    client_email = Column(String(30), nullable=False)
    contact_address = Column(String(1000), nullable=False)
    client_tel = Column(String(15), nullable=False)

    project_details = relationship("ProjectDetail", back_populates="client")



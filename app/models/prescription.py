from sqlalchemy import DateTime,ForeignKey,Column,String,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from app.database import Base 


class Prescription(Base):
    __tablename__="prescriptions"
    
    id:Mapped[int]=mapped_column(index=True,primary_key=True)
    patient_name:Mapped[str]=mapped_column(String)
    doctor_id:Mapped[int]=mapped_column(ForeignKey=("users.id"))
    created_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    
    doctor=relationship("User",back_populates="prescriptions")
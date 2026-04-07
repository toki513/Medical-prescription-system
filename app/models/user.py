from sqlalchemy import String,ForeignKey,Column,Boolean,DateTime,func
from sqlalchemy.orm import relationship,Mapped,mapped_column
import uuid
from datetime import datetime
from app.database import Base 


class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String)
    username:Mapped[str]=mapped_column(String)
    hashed_password:Mapped[str] =mapped_column(String)
    role:Mapped[str]=mapped_column(String,default="patient")
    is_active:Mapped[bool] = mapped_column(Boolean,default=True)
    created_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    
    
    prescriptions:Mapped[list[Prescription]]=relationship(
        "Prescription",
        back_populates="doctor",
        lazy="select",
        cascade="all,delete_orphan"
    )
    
    
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class PrescriptionCreate(BaseModel):
    patient_name:str
    medications:str
    
    
class PrescriptionResponse(BaseModel):
    id:UUID
    patient_name:str
    medication:str
    created_at:
    doctor_id:UUID
    
    model_config={"from_attributes":True}
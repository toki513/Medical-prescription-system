# app/routers/prescriptions.py
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.dependencies import CurrentUser, CurrentDoctor

router = APIRouter(prefix="/api/prescriptions", tags=["Prescriptions"])

DB = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=PrescriptionResponse, status_code=201)
async def create_prescription(
    data: PrescriptionCreate,
    db: DB,
    doctor: CurrentDoctor,       # Clean! Reads like plain English
):
    prescription = Prescription(**data.model_dump(), doctor_id=doctor.id)
    db.add(prescription)
    await db.flush()
    await db.refresh(prescription)
    return prescription

@router.get("/", response_model=List[PrescriptionResponse])
async def list_prescriptions(db: DB, current_user: CurrentUser):
    result = await db.execute(
        select(Prescription).where(Prescription.doctor_id == current_user.id)
    )
    return result.scalars().all()



@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(
    prescription_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Prescription).where(Prescription.id == prescription_id)
    )
    prescription = result.scalar_one_or_none()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.delete("/{prescription_id}", status_code=204)
async def delete_prescription(
    prescription_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    doctor: User = Depends(get_current_doctor)
):
    result = await db.execute(
        select(Prescription).where(
            Prescription.id == prescription_id,
            Prescription.doctor_id == doctor.id  # Can only delete YOUR prescriptions
        )
    )
    prescription = result.scalar_one_or_none()
    if not prescription:
        raise HTTPException(status_code=404, detail="Not found or not authorized")
    await db.delete(prescription)
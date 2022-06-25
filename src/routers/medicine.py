from fastapi import APIRouter, Depends

from database import Database
from dependencies import auth
from models.user import User
from schemas.medicine import TreatmentModel, NewConsumption

router = APIRouter(prefix="/treatment", tags=["Treatment"])


@router.post("/", status_code=201, summary="Add treatment")
async def add_treatment(
        treatment: TreatmentModel,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    TODO: Poner alguna descripcion xd
    """
    treatment = await User(db, user).add_treatment(treatment)
    return treatment


@router.post("/{treatment_id}/consumption", status_code=201, summary="Add consumption")
async def add_consumption(
        treatment_id: str,
        consumption: NewConsumption,
        user=Depends(auth.authenticate),
        db=Depends(Database.get_db),
):
    """
    TODO: Poner alguna descripcion xd
    """
    consumption = await User(db, user).add_consumption(treatment_id, consumption)
    return consumption

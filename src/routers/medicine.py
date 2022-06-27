from fastapi import APIRouter, Depends

from database import Database
from dependencies import auth
from models.user import User
from schemas.medicine import NewConsumption, TreatmentModel

router = APIRouter(prefix="/treatment", tags=["Treatment"])


@router.post("/", status_code=201, summary="Add treatment")
async def add_treatment(
    treatment: TreatmentModel,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Agrega un tratamiento
    """
    treatment = await User(db, user).add_treatment(treatment)
    return treatment


@router.get("/", status_code=200, summary="Get all treatments")
async def get_treatments(
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Obtiene todos los tratamientos
    """
    # TODO: @leilaspini esta funcion deberia quedar unicamente con las dos lineas de aca abajo descomentadas
    #       hay que implementar get_treatments en el modelo de User.
    #       La funcion debe devolver por defecto los tratamientos en un rango de +- 15 dias a partir de la fecha actual.
    #       Por otro lado, se debe incluir un parametro OPCIONAL para que se pueda cambiar esta fecha.
    #       Tambien hay que fijarse que los tratamientos deben devolverse con todas sus posibles consumiciones.
    #       No solamente las consumiciones que se han marcado (en la base de datos solamente guardamos las consumidas,
    #       pero hay que devolver las no consumidas tambien).

    # treatments = await User(db, user).get_treatments()
    # return treatments
    pass


@router.post(
    "/{treatment_id}/consumption", status_code=201, summary="Add a consumption"
)
async def add_consumption(
    treatment_id: str,
    consumption: NewConsumption,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Marca como consumida una medicina
    """
    consumption = await User(db, user).add_consumption(treatment_id, consumption)
    return consumption


@router.delete(
    "/{treatment_id}/consumption", status_code=200, summary="Delete a consumption"
)
async def delete_consumption(
    treatment_id: str,
    consumption: NewConsumption,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Elimina la consumición de una medicina
    """
    # TODO: cambiar el add_consumption para que se pueda eliminar una medicina que se ha consumido,
    #       que tenga un booleano por defecto
    # consumption = await User(db, user).add_consumption(treatment_id, consumption, delete=True)
    # return consumption
    pass

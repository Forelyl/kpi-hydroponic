from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from server.security.security import get_user
from server.security.dataclasses import User as UserInToken

from server.database_driver.dataclasses import Hydroponic_response, Hydroponic_input
import server.database_driver.database as database_manager


app = APIRouter(prefix="/api/hydroponic", tags=["hydroponic"])


@app.get("/all")
async def get_all_hydroponics(user: Annotated[UserInToken, Depends(get_user)]) -> list[Hydroponic_response]:
    result = await database_manager.get_all_hydroponics(user.id)
    return list(map(lambda hydroponic: Hydroponic_response.model_validate(hydroponic), result))


@app.get("/{hydroponic_id}")
async def get_hydroponic_by_id(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> Hydroponic_response | None:
    result = await database_manager.get_hydroponic_by_id(hydroponic_id, user.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hydroponic not found")
    return Hydroponic_response.model_validate(result)


@app.post("/add")
async def add_hydroponic(hydroponic_input: Hydroponic_input, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_hydroponic(hydroponic_input, user.id)


@app.patch("/reset/{hydroponic_id}")
async def reset_hydroponic(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.reset(hydroponic_id, user.id)


@app.delete("/{hydroponic_id}")
async def delete_hydroponic(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.delete_hydroponic(hydroponic_id, user.id)


# --- Update value for hydroponic ---


@app.patch("/{hydroponic_id}/update/water/add_10_percent")
async def add_10_percent_water(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_10_percent_water(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/minerals/add_5_percent")
async def add_5_percent_minerals(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_5_percent_minerals(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/temperature/add_1_celsius")
async def add_1_celsius_temperature(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_1_celsius_temperature(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/temperature/lower_1_celsius")
async def lower_1_celsius_temperature(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.lower_1_celsius_temperature(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/acidity/add_0_25")
async def add_0_25_acid(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_0_25_acid(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/acidity/lower_0_25")
async def lower_0_25_acid(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.lower_0_25_acid(hydroponic_id, user.id)


@app.patch("/{hydroponic_id}/update/oxygen/add_5_percent")
async def add_5_percent_oxygen(hydroponic_id: int, user: Annotated[UserInToken, Depends(get_user)]) -> None:
    await database_manager.add_5_percent_oxygen(hydroponic_id, user.id)
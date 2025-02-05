from sqlmodel import select, create_engine, Session # , SQLModel
import random
from fastapi import HTTPException, status

# also declaring dataclasses that seem to have a influence on this file (maybe)
from server.database_driver.dataclasses import User, Hydroponic, Hydroponic_input
from server.database_driver.dataclasses import HYDROPONIC_MIN_PH, HYDROPONIC_MAX_PH, HYDROPONIC_MAX_TEMPERATURE, HYDROPONIC_MIN_TEMPERATURE

from server.security.hasher_password import hash_password
from server.security.dataclasses import UserInDB

# playground imports
from threading import Event
from server.database_driver.iot_playground import playground_main


# --- Make an engine ---
def make_engine():
    username = "hydroponic-vsrhjvzrj"
    password = "vsrhjvzrj"
    hostname = "127.0.0.1"
    port = 1433
    database = "Hydroponic"

    connection_url = f"mssql+pymssql://{username}:{password}@{hostname}:{port}/{database}"
    engine = create_engine(connection_url, echo=False)
    # Don't know should I use it SQLModel.metadata.create_all(engine)
    return engine


__engine = make_engine()


# --- Playground starter ---
def start_playground(stop_event: Event):
    playground_main(__engine, stop_event)


# --- User table ----

async def get_user_by_username(username: str) -> UserInDB | None:
    with Session(__engine) as session:
        user = session.exec(select(User).where(User.username == username)).one_or_none()
        if user is None or user.id is None:
            return None

        return UserInDB(
            id=user.id,
            username=user.username,
            hashed_password=user.hash_salt
        )


async def get_user_by_id(id: int) -> UserInDB | None:
    with Session(__engine) as session:
        user = session.exec(select(User).where(User.id == id)).one_or_none()
        if user is None or user.id is None:
            return None

        return UserInDB(
            id=user.id,
            username=user.username,
            hashed_password=user.hash_salt
        )


async def check_username_exists(username: str) -> bool:
    with Session(__engine) as session:
        user = session.exec(select(User).where(User.username == username)).one_or_none()
        return user is not None


async def add_user(username: str, password: str) -> bool:
    if await check_username_exists(username):
        return False

    with Session(__engine) as session:
        user = User(
            username=username,
            hash_salt=hash_password(password),
            hydroponics=list()
        )
        session.add(user)
        session.commit()

    return True


async def delete_user(user_id: int) -> None:
    with Session(__engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not found")
        session.delete(user)
        session.commit()


# --- Hydroponic table ----

async def get_all_hydroponics(user_id: int) -> list[Hydroponic]:
    with Session(__engine) as session:
        hydroponics = session.exec(select(Hydroponic).where(Hydroponic.user_id_owner == user_id)).all()
        return list(hydroponics)


async def get_hydroponic_by_id(hydroponic_id: int, user_id: int) -> Hydroponic | None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return None
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        return hydroponic


async def add_hydroponic(hydroponic: Hydroponic_input, user_id: int) -> None:
    hydroponic_db = Hydroponic(
        name=hydroponic.name,
        user_id_owner=user_id,
        water_amount=hydroponic.water_amount,
        water_consumption=hydroponic.water_consumption,
        minerals_amount=hydroponic.minerals_amount,
        minerals_optimal=hydroponic.minerals_optimal,
        minerals_consumption=hydroponic.minerals_consumption,
        acidity_optimal_ph=hydroponic.acidity_optimal_ph,
        temperature_C_optimal=hydroponic.temperature_C_optimal,
        oxygen_amount=hydroponic.oxygen_amount,
        oxygen_consumption=hydroponic.oxygen_consumption,
        # Random
        value_water=random.uniform(0, hydroponic.water_amount),
        value_minerals=random.uniform(0, hydroponic.minerals_amount),
        value_acidity_ph=random.uniform(HYDROPONIC_MIN_PH, HYDROPONIC_MAX_PH),
        value_temperature_C=random.uniform(HYDROPONIC_MIN_TEMPERATURE, HYDROPONIC_MAX_TEMPERATURE),
        value_oxygen=random.uniform(0, hydroponic.oxygen_amount)
    )

    with Session(__engine) as session:
        session.add(hydroponic_db)
        session.commit()


async def add_10_percent_water(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_water = min(hydroponic.value_water + hydroponic.water_amount * 0.1, hydroponic.water_amount)
        session.add(hydroponic)
        session.commit()


async def add_5_percent_minerals(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_minerals = min(hydroponic.value_minerals + hydroponic.minerals_amount * 0.05, hydroponic.minerals_amount)
        session.add(hydroponic)
        session.commit()


async def add_1_celsius_temperature(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_temperature_C = min(hydroponic.value_temperature_C + 1, HYDROPONIC_MAX_TEMPERATURE)
        session.add(hydroponic)
        session.commit()


async def lower_1_celsius_temperature(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_temperature_C = max(hydroponic.value_temperature_C - 1, HYDROPONIC_MIN_TEMPERATURE)
        session.add(hydroponic)
        session.commit()


async def add_0_25_acid(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_acidity_ph = max(hydroponic.value_acidity_ph - 0.25, HYDROPONIC_MIN_PH)
        session.add(hydroponic)
        session.commit()


async def lower_0_25_acid(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_acidity_ph = min(hydroponic.value_acidity_ph + 0.25, HYDROPONIC_MAX_PH)
        session.add(hydroponic)
        session.commit()


async def add_5_percent_oxygen(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_oxygen = min(hydroponic.value_oxygen + hydroponic.oxygen_amount * 0.05, hydroponic.oxygen_amount)
        session.add(hydroponic)
        session.commit()


async def reset(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        hydroponic.value_water = random.uniform(0, hydroponic.water_amount)
        hydroponic.value_minerals = random.uniform(0, hydroponic.minerals_amount)
        hydroponic.value_acidity_ph = random.uniform(HYDROPONIC_MIN_PH, HYDROPONIC_MAX_PH)
        hydroponic.value_temperature_C = random.uniform(HYDROPONIC_MIN_TEMPERATURE, HYDROPONIC_MAX_TEMPERATURE)
        hydroponic.value_oxygen = random.uniform(0, hydroponic.oxygen_amount)
        session.add(hydroponic)
        session.commit()


async def delete_hydroponic(hydroponic_id: int, user_id: int) -> None:
    with Session(__engine) as session:
        hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one_or_none()
        if hydroponic is None:
            return
        if hydroponic.user_id_owner != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this hydroponic")

        session.delete(hydroponic)
        session.commit()
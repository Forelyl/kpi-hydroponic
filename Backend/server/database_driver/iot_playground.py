import threading
import random
import time
from sqlmodel import Session, select

from server.database_driver.dataclasses import Hydroponic, HYDROPONIC_MIN_TEMPERATURE, HYDROPONIC_MAX_TEMPERATURE, HYDROPONIC_MIN_PH, HYDROPONIC_MAX_PH

__SLEEP_TIME                    = 10
__RANDOM_CHANGE_PERCENTAGE      = 0.05
__RANDOM_ACIDITY_MAX_CHANGE     = (HYDROPONIC_MAX_PH - HYDROPONIC_MIN_PH) * __RANDOM_CHANGE_PERCENTAGE
__RANDOM_TEMPERATURE_MAX_CHANGE = (HYDROPONIC_MAX_TEMPERATURE - HYDROPONIC_MIN_TEMPERATURE) * __RANDOM_CHANGE_PERCENTAGE


# Periodic function to imitate IoT
def playground_main(engine, stop_conditionalvar: threading.Event):
    while not stop_conditionalvar.is_set():
        with Session(engine) as session:
            hydroponics = list(session.exec(select(Hydroponic)).all())
            for x in hydroponics:
                __update_hydroponic_caller(engine, x.id)
        time.sleep(__SLEEP_TIME)  # Wait one minute


def __update_hydroponic_caller(engine, hydroponic_id):
    with Session(engine) as session:
        try:
            with session.begin():  # Begin a transaction
                hydroponic = session.exec(select(Hydroponic).where(Hydroponic.id == hydroponic_id)).one()
                if hydroponic is None:
                    print(f"Playground: Hydroponic with id {hydroponic_id} does not exist")
                    return

                __update_hydroponic(hydroponic)
                session.add(hydroponic)
        except Exception as e:
            session.rollback()  # Rollback on any error
            print(f"Playground: Failed to update hydroponic {hydroponic_id}: {e}")


def __update_hydroponic(hydroponic: Hydroponic):
    hydroponic.value_water      = max(0, hydroponic.value_water    - hydroponic.water_consumption    * __SLEEP_TIME)
    hydroponic.value_minerals   = max(0, hydroponic.value_minerals - hydroponic.minerals_consumption * __SLEEP_TIME)
    hydroponic.value_oxygen     = max(0, hydroponic.value_oxygen   - hydroponic.oxygen_consumption   * __SLEEP_TIME)

    # --- Acidity ---
    old_value     = hydroponic.value_acidity_ph
    changed_value = random.uniform(-__RANDOM_ACIDITY_MAX_CHANGE, __RANDOM_ACIDITY_MAX_CHANGE)
    new_value     = max(HYDROPONIC_MIN_PH, min(HYDROPONIC_MAX_PH, old_value + changed_value))

    hydroponic.value_acidity_ph = new_value

    # --- Temperature ---
    old_value     = hydroponic.value_temperature_C
    changed_value = random.uniform(-__RANDOM_TEMPERATURE_MAX_CHANGE, __RANDOM_TEMPERATURE_MAX_CHANGE)
    new_value     = max(HYDROPONIC_MIN_TEMPERATURE, min(HYDROPONIC_MAX_TEMPERATURE, old_value + changed_value))

    hydroponic.value_temperature_C = new_value
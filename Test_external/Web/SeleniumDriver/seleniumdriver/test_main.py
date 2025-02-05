import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import base64
import json
import random


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5173/")
    yield
    driver.close()
    driver.quit()


def get_login_from_json_web_token(token: str):
    try:
        # Split the JWT into its components: header, payload, and signature
        header, payload, signature = token.split('.')

        # Decode the payload from base64url format
        padded_payload = payload + '=' * (-len(payload) % 4)  # Add padding if needed
        decoded_payload = base64.urlsafe_b64decode(padded_payload).decode('utf-8')

        # Convert the JSON string to a Python dictionary
        payload_dict = json.loads(decoded_payload)
        return payload_dict
    except Exception as e:
        pytest.fail(f"Error decoding JSON Web Token: {e}")


def test_login(test_setup):
    title = driver.title
    assert title == "EmeraldWater - login", "First page should be login page"

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text'][@id='login']")))
    input_login: WebElement = driver.find_element(By.XPATH, "//input[@type='text'][@id='login']")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password'][@id='password']")))
    input_password: WebElement = driver.find_element(By.XPATH, "//input[@type='password'][@id='password']")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
    submit_button: WebElement = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")

    input_login.send_keys("Mia")
    input_password.send_keys("secret")

    submit_button.click()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - hydroponics list")

    token = driver.execute_script("return localStorage.getItem('authToken');")
    assert token is not None, "Login failed, no token"
    token_info = get_login_from_json_web_token(token)
    assert token_info['sub'] == 'Mia', "Login failed, wrong login in token"


def test_signup(test_setup):
    title = driver.title
    assert title == "EmeraldWater - login", "First page should be login page"

    to_sign_up_button: WebElement = driver.find_element(By.XPATH, "//button[@id='to-sign-up']")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(to_sign_up_button))
    to_sign_up_button.click()

    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - sign up")

    input_login: WebElement = driver.find_element(By.XPATH, "//input[@type='text'][@id='login']")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(input_login))

    input_password: WebElement = driver.find_element(By.XPATH, "//input[@type='password'][@id='password']")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(input_password))

    submit_button: WebElement = driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(submit_button))

    username = f"TestUser.{random.randint(1, 100000)}"
    input_login.send_keys(username)
    input_password.send_keys("secret")

    submit_button.click()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - hydroponics list")

    token = driver.execute_script("return localStorage.getItem('authToken');")
    assert token is not None, "Sign up failed, no token"
    token_info = get_login_from_json_web_token(token)
    assert token_info['sub'] == username, "Sign up failed, wrong login in token"


def test_readdress(test_setup):
    driver.get("http://127.0.0.1:5173/")
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")
    driver.get("http://127.0.0.1:5173/src/pages/new/new.html")
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")
    driver.get("http://127.0.0.1:5173/src/pages/logout/logout.html")
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")
    driver.get("http://127.0.0.1:5173/src/pages/operating/operating.html?element=1034")
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")


@pytest.fixture()
def test_logined_setup(test_setup):
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "login")))
    input_login: WebElement = driver.find_element(By.ID, "login")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "password")))
    input_password: WebElement = driver.find_element(By.ID, "password")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "apply-button")))
    submit_button: WebElement = driver.find_elements(By.TAG_NAME, "button")[1]

    input_login.send_keys("Mia")
    input_password.send_keys("secret")

    submit_button.click()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - hydroponics list")


def test_unlogin(test_logined_setup):
    driver.get("http://127.0.0.1:5173/src/pages/logout/logout.html")
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - logout")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "base-rectangle-button")))
    button_logout: WebElement = driver.find_element(By.CLASS_NAME, "base-rectangle-button")

    button_logout.click()

    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - login")
    assert driver.title == "EmeraldWater - login",  "First page after logout should be login page"

    token = driver.execute_script("return localStorage.getItem('authToken');")
    assert token is None, "Logout failed, token still exists"


class New_page_inputs:
    def __init__(self, inputs: list[WebElement]):
        self.name = inputs[0]
        self.water_amount = inputs[1]
        self.water_consumption_speed = inputs[2]

        self.minerals_amount = inputs[3]
        self.mineral_optimal_amount = inputs[4]
        self.mineral_consumption_speed = inputs[5]

        self.oxygen_amount = inputs[6]
        self.oxygen_consumption_speed = inputs[7]

        self.acidness_optimal_amount = inputs[8]
        self.temperature_optimal_amount = inputs[9]


def get_inputs_from_new_page() -> New_page_inputs:
    trio_inputs = driver.find_elements(By.TAG_NAME, "trio-input")
    assert len(trio_inputs) == 4, "Not 4 trio-inputs"

    inputs = []
    for i in range(len(trio_inputs)):
        inputs_temp = trio_inputs[i].shadow_root.find_elements(By.CSS_SELECTOR, '.input-group:not([style*="display: none"]) input')
        for x in inputs_temp:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(x))
        inputs.extend(inputs_temp)

    assert len(inputs) == 10, inputs
    return New_page_inputs(inputs)


def add_hydroponic_sub(is_empty_add: bool = False) -> str:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.add-new-button")))
    button_add_hydroponic: WebElement = driver.find_element(By.CSS_SELECTOR, "a.add-new-button")

    button_add_hydroponic.click()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - add new hydroponic")

    test_title = "Test hydroponic " + str(random.randint(1, 1000000))

    if is_empty_add:
        input_values = [
            test_title, "1000", "0.001", "1000", "10",
            "0.001", "1000", "0.001", "7.3", "16"
        ]
    else:
        input_values = [
            test_title, "1000", "10", "1000", "10",
            "10", "1000", "10", "7.3", "16"
        ]

    inputs = get_inputs_from_new_page()
    inputs.name.send_keys(input_values[0])
    inputs.water_amount.send_keys(input_values[1])
    inputs.water_consumption_speed.send_keys(input_values[2])
    inputs.minerals_amount.send_keys(input_values[3])
    inputs.mineral_optimal_amount.send_keys(input_values[4])
    inputs.mineral_consumption_speed.send_keys(input_values[5])
    inputs.oxygen_amount.send_keys(input_values[6])
    inputs.oxygen_consumption_speed.send_keys(input_values[7])
    inputs.acidness_optimal_amount.send_keys(input_values[8])
    inputs.temperature_optimal_amount.send_keys(input_values[9])

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "apply-button")))
    button_add_hydroponic: WebElement = driver.find_element(By.ID, "apply-button")
    button_add_hydroponic.click()

    return test_title


def delete_hydroponic_sub():
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "button-delete")))
    button_delete: WebElement = driver.find_element(By.ID, "button-delete")
    button_delete.click()


def test_add_delete_hydroponic(test_logined_setup):
    test_title = add_hydroponic_sub()

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//hydroponic-iter[@name='{test_title}']")))
    hydroponic_element: WebElement = driver.find_element(By.XPATH, f"//hydroponic-iter[@name='{test_title}']")

    hydroponic_element.click()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == f"EmeraldWater - operating {test_title}")

    delete_hydroponic_sub()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - hydroponics list")

    list_hydroponic_element: list[WebElement] = driver.find_elements(By.XPATH, f"//hydroponic-iter[@name='{test_title}']")
    assert len(list_hydroponic_element) == 0, "Hydroponic was not deleted"


@pytest.fixture()
def test_control_page(test_logined_setup):
    # Add and open
    test_title = add_hydroponic_sub(True)

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//hydroponic-iter[@name='{test_title}']")))
    hydroponic_element: WebElement = driver.find_element(By.XPATH, f"//hydroponic-iter[@name='{test_title}']")
    hydroponic_element.click()

    yield

    # Delete
    delete_hydroponic_sub()
    WebDriverWait(driver, 10).until(lambda driver: driver.title == "EmeraldWater - hydroponics list")

    list_hydroponic_element: list[WebElement] = driver.find_elements(By.XPATH, f"//hydroponic-iter[@name='{test_title}']")
    assert len(list_hydroponic_element) == 0, "Hydroponic was not deleted"


class Control_page:
    def __init__(self):
        # water
        self.water_indicator = driver.find_element(By.ID, "water-tank-progress-bar")
        WebDriverWait(driver, 3).until(lambda driver: self.water_indicator.is_displayed())

        self.water_increase_button = driver.find_element(By.ID, "button-add-water")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.water_increase_button))

        # minerals
        self.mineral_indicator = driver.find_element(By.ID, "mineral-progress-bar")
        WebDriverWait(driver, 3).until(lambda driver: self.mineral_indicator.is_displayed())

        self.mineral_increase_button = driver.find_element(By.ID, "button-add-mineral")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.mineral_increase_button))

        # temperature
        self.temperature_indicator = driver.find_element(By.ID, "temperature-progress-bar")
        WebDriverWait(driver, 3).until(lambda driver: self.temperature_indicator.is_displayed())

        self.temperature_increase_button = driver.find_element(By.ID, "button-add-temperature")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.temperature_increase_button))

        self.temperature_decrease_button = driver.find_element(By.ID, "button-lower-temperature")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.temperature_decrease_button))

        # acidndness
        self.acidness_indicator = driver.find_element(By.ID, "acidity-progress-bar")
        WebDriverWait(driver, 3).until(lambda driver: self.acidness_indicator.is_displayed())

        self.acidness_increase_button = driver.find_element(By.ID, "button-add-acidity")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.acidness_increase_button))

        self.acidness_decrease_button = driver.find_element(By.ID, "button-lower-acidity")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.acidness_decrease_button))

        # oxygen
        self.oxygen_indicator = driver.find_element(By.ID, "oxygen-progress-bar")
        WebDriverWait(driver, 3).until(lambda driver: self.oxygen_indicator.is_displayed())

        self.oxygen_increase_button = driver.find_element(By.ID, "button-add-oxygen")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.oxygen_increase_button))

        # controls
        self.reload_button = driver.find_element(By.ID, "button-reload")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.reload_button))

        self.delete_button = driver.find_element(By.ID, "button-delete")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(self.delete_button))

    def get_water_percentage(self) -> float:
        water_percentage_str = self.water_indicator.get_attribute("percentage")
        assert water_percentage_str is not None, "Water percentage attribute is None"
        water_percentage = float(water_percentage_str)
        return water_percentage

    def get_mineral_percentage(self) -> float:
        mineral_percentage_str = self.mineral_indicator.get_attribute("percentage")
        assert mineral_percentage_str is not None, "Mineral percentage attribute is None"
        mineral_percentage = float(mineral_percentage_str)
        return mineral_percentage

    def get_temperature_percentage(self) -> float:
        temperature_percentage_str = self.temperature_indicator.get_attribute("percentage")
        assert temperature_percentage_str is not None, "Temperature percentage attribute is None"
        temperature_percentage = float(temperature_percentage_str)
        return temperature_percentage

    def get_acidness_percentage(self) -> float:
        acidness_percentage_str = self.acidness_indicator.get_attribute("percentage")
        assert acidness_percentage_str is not None, "Acidness percentage attribute is None"
        acidness_percentage = float(acidness_percentage_str)
        return acidness_percentage

    def get_oxygen_percentage(self) -> float:
        oxygen_percentage_str = self.oxygen_indicator.get_attribute("percentage")
        assert oxygen_percentage_str is not None, "Oxygen percentage attribute is None"
        oxygen_percentage = float(oxygen_percentage_str)
        return oxygen_percentage


def test_reload_button(test_control_page):
    control_page = Control_page()

    water_percentage       = control_page.get_water_percentage()
    mineral_percentage     = control_page.get_mineral_percentage()
    temperature_percentage = control_page.get_temperature_percentage()
    acidness_percentage    = control_page.get_acidness_percentage()
    oxygen_percentage      = control_page.get_oxygen_percentage()

    # RELOAD
    control_page.reload_button.click()
    WebDriverWait(driver, 3).until(lambda driver: water_percentage != control_page.get_water_percentage())

    water_percentage_new       = control_page.get_water_percentage()
    mineral_percentage_new     = control_page.get_mineral_percentage()
    temperature_percentage_new = control_page.get_temperature_percentage()
    acidness_percentage_new    = control_page.get_acidness_percentage()
    oxygen_percentage_new      = control_page.get_oxygen_percentage()

    # Checks
    assert abs(water_percentage - water_percentage_new) > 0.01, "Water percentage is not changed, or bad random"
    assert abs(mineral_percentage - mineral_percentage_new) > 0.01, "Mineral percentage is not changed, or bad random"
    assert abs(temperature_percentage - temperature_percentage_new) > 0.01, "Temperature percentage is not changed, or bad random"
    assert abs(acidness_percentage - acidness_percentage_new) > 0.01, "Acidness percentage is not changed, or bad random"
    assert abs(oxygen_percentage - oxygen_percentage_new) > 0.01, "Oxygen percentage is not changed, or bad random"


def test_water_operation(test_control_page):
    control_page = Control_page()
    water_percentage = control_page.get_water_percentage()
    while water_percentage > 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: water_percentage != control_page.get_water_percentage())
        water_percentage = control_page.get_water_percentage()

    for i in range(10):
        control_page.water_increase_button.click()

    WebDriverWait(driver, 3).until(lambda driver: water_percentage != control_page.get_water_percentage())
    water_percentage = control_page.get_water_percentage()

    assert water_percentage >= 95, "Water percentage is not increased"


def test_mineral_operation(test_control_page):
    control_page = Control_page()
    mineral_percentage = control_page.get_mineral_percentage()
    while mineral_percentage > 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: mineral_percentage != control_page.get_mineral_percentage())
        mineral_percentage = control_page.get_mineral_percentage()

    for i in range(20):
        control_page.mineral_increase_button.click()

    WebDriverWait(driver, 3).until(lambda driver: mineral_percentage != control_page.get_mineral_percentage())
    mineral_percentage = control_page.get_mineral_percentage()

    assert mineral_percentage >= 95, "Mineral percentage is not increased"


def test_oxygen_operation(test_control_page):
    control_page = Control_page()
    oxygen_percentage = control_page.get_oxygen_percentage()
    while oxygen_percentage > 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: oxygen_percentage != control_page.get_oxygen_percentage())
        oxygen_percentage = control_page.get_oxygen_percentage()

    for i in range(20):
        control_page.oxygen_increase_button.click()

    WebDriverWait(driver, 3).until(lambda driver: oxygen_percentage != control_page.get_oxygen_percentage())
    oxygen_percentage = control_page.get_oxygen_percentage()


def test_temperature_operation(test_control_page):
    control_page = Control_page()
    temperature_percentage = control_page.get_temperature_percentage()

    # Test increase
    while temperature_percentage > 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: temperature_percentage != control_page.get_temperature_percentage())
        temperature_percentage = control_page.get_temperature_percentage()

    for i in range(20):
        control_page.temperature_increase_button.click()

    WebDriverWait(driver, 3).until(lambda driver: temperature_percentage != control_page.get_temperature_percentage())
    temperature_percentage = control_page.get_temperature_percentage()
    assert temperature_percentage >= 95, "Temperature percentage is not increased"

    # Test decrease
    while temperature_percentage < 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: temperature_percentage != control_page.get_temperature_percentage())
        temperature_percentage = control_page.get_temperature_percentage()

    for i in range(20):
        control_page.temperature_decrease_button.click()

    WebDriverWait(driver, 3).until(lambda driver: temperature_percentage != control_page.get_temperature_percentage())
    temperature_percentage = control_page.get_temperature_percentage()
    assert temperature_percentage <= 5, "Temperature percentage is not decreased"


def test_acidness_operation(test_control_page):
    control_page = Control_page()
    acidness_percentage = control_page.get_acidness_percentage()

    # Test increase - is reversed to other due to how accidness is represented
    while acidness_percentage < 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: acidness_percentage != control_page.get_acidness_percentage())
        acidness_percentage = control_page.get_acidness_percentage()

    for i in range(64):
        control_page.acidness_increase_button.click()

    WebDriverWait(driver, 3).until(lambda driver: acidness_percentage != control_page.get_acidness_percentage())
    acidness_percentage = control_page.get_acidness_percentage()
    assert acidness_percentage <= 5, "Acidness percentage is not increased"

    # Test decrease - is reversed to other due to how accidness is represented
    while acidness_percentage > 50:
        control_page.reload_button.click()
        WebDriverWait(driver, 3).until(lambda driver: acidness_percentage != control_page.get_acidness_percentage())
        acidness_percentage = control_page.get_acidness_percentage()

    for i in range(64):
        control_page.acidness_decrease_button.click()

    WebDriverWait(driver, 3).until(lambda driver: acidness_percentage != control_page.get_acidness_percentage())
    acidness_percentage = control_page.get_acidness_percentage()
    assert acidness_percentage >= 95, "Acidness percentage is not decreased"
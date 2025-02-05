import unittest
from unittest.mock import AsyncMock, patch

from server.security.dataclasses import User, UserInDB
from server.security.json_web_token import process_access_token
from server.security.security import add_token_endpoint, add_test_endpoint
from fastapi.testclient import TestClient

FAKE_USER_ID = 1
FAKE_USER_USERNAME = "test_user"


class FakeHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return password  # Just returns the same password (no real hashing).

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return password == hashed_password  # Compares directly without hashing.


class TestHydroponicAPI(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Mock Database
        cls.db_mock = AsyncMock()
        cls.database_patcher  = patch("server.database_driver.database", cls.db_mock)
        cls.database_patcher2 = patch("server.security.security.database_manager", cls.db_mock)

        cls.database_patcher.start()
        cls.database_patcher2.start()

        from server.main import app # should be after db mock

        # Fake Hasher
        cls.hasher_fake = patch("server.security.hasher_password.hash_password", FakeHasher.hash_password)
        cls.verifier_fake = patch("server.security.hasher_password.verify_password", FakeHasher.verify_password)

        cls.hasher_fake.start()
        cls.verifier_fake.start()

        # Stub JWT
        app.dependency_overrides[process_access_token] = lambda: User(id=FAKE_USER_ID, username=FAKE_USER_USERNAME)

        cls.stub_jwt_generate = patch(
            "server.security.json_web_token.generate_access_token",
            lambda *args, **kwargs: "fake_token"
        )
        cls.stub_jwt_generate.start()

        # Add token and test endpoints
        add_token_endpoint(app)
        add_test_endpoint(app)

        # Test client
        cls.client = TestClient(app)

    def setUp(self):
        # Reset mocks
        self.db_mock.reset_mock()

    @classmethod
    def tearDownClass(cls):
        cls.database_patcher.stop()
        cls.database_patcher2.stop()
        cls.hasher_fake.stop()
        cls.stub_jwt_generate.stop()
        cls.verifier_fake.stop()

    async def test_get_all_hydroponics(self):
        # Simulate mocked database returning hydroponic data
        from server.database_driver.dataclasses import Hydroponic_response
        self.db_mock.get_all_hydroponics.return_value = [
            Hydroponic_response(
                id=1, name="Arm1", water_amount=1000, water_consumption=1,
                minerals_amount=12, minerals_optimal=12, minerals_consumption=12,
                acidity_optimal_ph=12, temperature_C_optimal=12, oxygen_amount=12,
                oxygen_consumption=12, value_water=12, value_minerals=12,
                value_acidity_ph=12, value_temperature_C=12, value_oxygen=12
            ),
            Hydroponic_response(
                id=2, name="Arm2", water_amount=1000, water_consumption=1,
                minerals_amount=12, minerals_optimal=12, minerals_consumption=12,
                acidity_optimal_ph=12, temperature_C_optimal=12, oxygen_amount=12,
                oxygen_consumption=12, value_water=12, value_minerals=12,
                value_acidity_ph=12, value_temperature_C=12, value_oxygen=12
            )
        ]

        # Make API call
        response = self.client.get("/api/hydroponic/all", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.get_all_hydroponics.assert_called_once_with(FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "Arm1")

    async def test_generate_token(self):
        # Prepare a mocked UserInDB object
        mocked_user = UserInDB(
            id=FAKE_USER_ID,
            username=FAKE_USER_USERNAME,
            hashed_password=FakeHasher.hash_password("password")  # Match the expected value for password verification
        )

        # Mock the get_user_by_username method to return the mocked_user
        self.db_mock.get_user_by_username.return_value = mocked_user

        # Call the token endpoint with the correct data
        response = self.client.post("/token", data={"username": FAKE_USER_USERNAME, "password": FakeHasher.hash_password("password")})
        self.db_mock.get_user_by_username.assert_called_once_with(FAKE_USER_USERNAME)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["access_token"], "fake_token")

    async def test_delete_hydroponic(self):
        # Simulate mocked database deleting hydroponic data
        self.db_mock.delete_hydroponic.return_value = True

        # Make API call
        response = self.client.delete("/api/hydroponic/1", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.delete_hydroponic.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_get_hydroponic_found(self):
        from server.database_driver.dataclasses import Hydroponic_response
        # Simulate mocked database returning hydroponic data
        self.db_mock.get_hydroponic_by_id.return_value = Hydroponic_response(
            id=1, name="Arm1", water_amount=1000, water_consumption=1,
            minerals_amount=12, minerals_optimal=12, minerals_consumption=12,
            acidity_optimal_ph=12, temperature_C_optimal=12, oxygen_amount=12,
            oxygen_consumption=12, value_water=12, value_minerals=12,
            value_acidity_ph=12, value_temperature_C=12, value_oxygen=12
        )
        # Make API call
        response = self.client.get("/api/hydroponic/1", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.get_hydroponic_by_id.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Arm1")
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["water_amount"], 1000)
        self.assertEqual(response.json()["water_consumption"], 1)
        self.assertEqual(response.json()["minerals_amount"], 12)
        self.assertEqual(response.json()["minerals_optimal"], 12)
        self.assertEqual(response.json()["minerals_consumption"], 12)
        self.assertEqual(response.json()["acidity_optimal_ph"], 12)
        self.assertEqual(response.json()["temperature_C_optimal"], 12)
        self.assertEqual(response.json()["oxygen_amount"], 12)
        self.assertEqual(response.json()["oxygen_consumption"], 12)
        self.assertEqual(response.json()["value_water"], 12)
        self.assertEqual(response.json()["value_minerals"], 12)
        self.assertEqual(response.json()["value_acidity_ph"], 12)
        self.assertEqual(response.json()["value_temperature_C"], 12)
        self.assertEqual(response.json()["value_oxygen"], 12)

    async def test_get_hydroponic_not_found(self):
        # Simulate mocked database returning None
        self.db_mock.get_hydroponic_by_id.return_value = None

        # Make API call
        response = self.client.get("/api/hydroponic/1", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.get_hydroponic_by_id.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Hydroponic not found"})

    async def test_add_hydroponic(self):
        # Simulate mocked database adding hydroponic data
        from server.database_driver.dataclasses import Hydroponic_input
        self.db_mock.add_hydroponic.return_value = True

        input_obj = Hydroponic_input(
            name="Arm1", water_amount=1000, water_consumption=1,
            minerals_amount=12, minerals_optimal=12, minerals_consumption=12,
            acidity_optimal_ph=12, temperature_C_optimal=12, oxygen_consumption=12,
            oxygen_amount=12
        )

        # Make API callq
        response = self.client.post("/api/hydroponic/add", json=input_obj.model_dump(), headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_hydroponic.assert_called_once_with(input_obj,  FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_reset_hydroponic(self):
        # Simulate mocked database resetting hydroponic data
        self.db_mock.reset.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/reset/1", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.reset.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_add_10_percent_water(self):
        # Simulate mocked database adding 10% water
        self.db_mock.add_10_percent_water.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/water/add_10_percent", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_10_percent_water.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_add_5_percent_minerals(self):
        # Simulate mocked database adding 5% minerals
        self.db_mock.add_5_percent_minerals.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/minerals/add_5_percent", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_5_percent_minerals.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_add_1_celsius_temperature(self):
        # Simulate mocked database adding 1 celsius temperature
        self.db_mock.add_1_celsius_temperature.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/temperature/add_1_celsius", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_1_celsius_temperature.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_lower_1_celsius_temperature(self):
        # Simulate mocked database adding 1 celsius temperature
        self.db_mock.lower_1_celsius_temperature.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/temperature/lower_1_celsius", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.lower_1_celsius_temperature.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_add_0_25_acid(self):
        # Simulate mocked database adding 0.25 acid
        self.db_mock.add_0_25_acid.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/acidity/add_0_25", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_0_25_acid.assert_called_once_with(1, FAKE_USER_ID)\

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_lower_0_25_acid(self):
        # Simulate mocked database adding 0.25 acid
        self.db_mock.lower_0_25_acid.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/acidity/lower_0_25", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.lower_0_25_acid.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_add_5_percent_oxygen(self):
        # Simulate mocked database adding 5% oxygen
        self.db_mock.add_5_percent_oxygen.return_value = True

        # Make API call
        response = self.client.patch("/api/hydroponic/1/update/oxygen/add_5_percent", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.add_5_percent_oxygen.assert_called_once_with(1, FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_register(self):
        # Simulate mocked database adding user
        self.db_mock.add_user.return_value = True
        self.db_mock.get_user_by_username.return_value = UserInDB(id=1, username=FAKE_USER_USERNAME, hashed_password=FakeHasher.hash_password("password"))

        # Make API call
        response = self.client.post("/register", data={
            "username": FAKE_USER_USERNAME,
            "password": "password"
        })
        self.db_mock.add_user.assert_called_once_with(FAKE_USER_USERNAME, "password")
        self.db_mock.get_user_by_username.assert_called_once_with(FAKE_USER_USERNAME)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'access_token': 'fake_token', 'token_type': 'bearer'})

    async def test_user_exist(self):
        # Simulate mocked database checking username
        self.db_mock.check_username_exists.return_value = True

        # Make API call
        response = self.client.get(f"/user/exists?username={FAKE_USER_USERNAME}")
        self.db_mock.check_username_exists.assert_called_once_with(FAKE_USER_USERNAME)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), True)

    async def test_delete_user(self):
        # Simulate mocked database deleting user
        self.db_mock.delete_user.return_value = True

        # Make API call
        response = self.client.delete("/user", headers={"Authorization": "Bearer fake_token"})
        self.db_mock.delete_user.assert_called_once_with(FAKE_USER_ID)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), None)

    async def test_read_users_me(self):
        # Make API call
        response = self.client.get("/users/me", headers={"Authorization": "Bearer fake_token"})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": FAKE_USER_ID, "username": FAKE_USER_USERNAME})

    async def test_register_user_already_exists(self):
        # Simulate mocked database adding user
        self.db_mock.add_user.return_value = False

        # Make API call
        response = self.client.post("/register", data={
            "username": FAKE_USER_USERNAME,
            "password": "testpassword"
        })
        self.db_mock.add_user.assert_called_once_with(FAKE_USER_USERNAME, "testpassword")

        # Assertions
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"detail": "User already exists"})
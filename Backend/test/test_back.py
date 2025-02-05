# WARNING if test fails check database that is been tested
# USER - Username: Mia, password: secret | should exist

import unittest

from fastapi import HTTPException
import random
import asyncio

from server.database_driver.dataclasses import Hydroponic, Hydroponic_input
from server.security.dataclasses import UserInDB
import server.security.hasher_password as hasher
import server.security.json_web_token as token_provider
import server.security.security as security
import server.database_driver.database as database_manager

TEST_USERNAME   = "Mia"    # shoud be real user in database
TEST_PASSWORD   = "secret" # shoud be real user in database
TEST_HYDROPONIC = Hydroponic_input(
    name="test xHydro3456",
    water_amount=1000,
    water_consumption=1,
    minerals_amount=1000,
    minerals_optimal=1,
    minerals_consumption=1,
    acidity_optimal_ph=7,
    temperature_C_optimal=19,
    oxygen_amount=1000,
    oxygen_consumption=1
)


class TestServer(unittest.TestCase):

    def test_hash(self):
        test1 = hasher.hash_password("test")
        test2 = hasher.hash_password("test")
        wrong = hasher.hash_password("wrong")

        self.assertNotEqual(test1, test2, "The same password hashed should not be the same, yet may")
        self.assertNotEqual(test1, wrong, "Different passwords hashed should not be the same, yet may")
        self.assertNotEqual(test2, wrong, "Different passwords hashed should not be the same, yet may")

        result1       = hasher.verify_password("test",  test1)
        result2       = hasher.verify_password("test",  test2)
        result3       = hasher.verify_password("wrong", wrong)
        result3_error = hasher.verify_password("test",  wrong)

        self.assertTrue(result1, "The password should be verified")
        self.assertTrue(result2, "The password should be verified")
        self.assertTrue(result3, "TThe password should be verified")
        self.assertFalse(result3_error, "The password should not be verified")


class TestAsyncServer(unittest.IsolatedAsyncioTestCase):
    # # Check if the user exists in the database
    # database_user = await database_manager.get_user_by_id(user_id)
    # if database_user is None or database_user.username != username:
    #     raise credentials_exception

    async def test_json_web_token_correct_user(self):
        database_user = await database_manager.get_user_by_username(TEST_USERNAME)
        if database_user is None:
            self.fail(f"User {TEST_USERNAME} is absent from Database")

        correct_user = {
            "sub": TEST_USERNAME,
            "id": database_user.id
        }

        token_correct_user  = token_provider.generate_access_token(correct_user)
        correct_user_result = await token_provider.process_access_token(token_correct_user)

        self.assertEqual(correct_user_result.id, database_user.id, "Provided username should be equal to what ws returned")
        self.assertEqual(correct_user_result.username, TEST_USERNAME, "Provided id should be equal to what ws returned")

    async def test_json_web_token_invalid_token(self):
        try:
            await token_provider.process_access_token("incorrect_token")
        except HTTPException:
            pass
        else:
            self.fail("Incorrect token has passed")

    async def test_json_web_token_null_userinfo(self):
        # values aren't important in this case - it should raise in any case
        none_user1 = {
            "sub": None,
            "id": 1
        }
        token1  = token_provider.generate_access_token(none_user1)
        none_user2 = {
            "sub": "Some value",
            "id": None
        }
        token2  = token_provider.generate_access_token(none_user2)
        none_user3 = {
            "sub": None,
            "id": None
        }
        token3  = token_provider.generate_access_token(none_user3)

        try:
            await token_provider.process_access_token(token1)
        except HTTPException:
            pass
        else:
            self.fail("Incorrect token (sub: None) has passed")

        try:
            await token_provider.process_access_token(token2)
        except HTTPException:
            pass
        else:
            self.fail("Incorrect token (id: None) has passed")

        try:
            await token_provider.process_access_token(token3)
        except HTTPException:
            pass
        else:
            self.fail("Incorrect token (sub: None and id: None) has passed")

    async def test_json_web_token_incorrect_username(self):
        # values aren't important in this case - it should raise in any case
        database_correct_user = await database_manager.get_user_by_username(TEST_USERNAME)
        if database_correct_user is None:
            self.fail(f"User {TEST_USERNAME} is absent from Database")
        bad_user = {
            "sub": TEST_USERNAME + "wrong",
            "id": database_correct_user.id
        }
        token = token_provider.generate_access_token(bad_user)
        try:
            await token_provider.process_access_token(token)
        except HTTPException:
            pass
        else:
            self.fail("Incorrect token (username doesn't align with id) has passed")

    async def test_security_user_authentification_point(self):
        username = TEST_USERNAME
        password = TEST_PASSWORD

        await security.authenticate_user(username, password)

        fake_password = "wrong" + password

        with self.assertRaises(HTTPException):
            await security.authenticate_user(username, fake_password)

        fake_username = "wrong" + username
        with self.assertRaises(HTTPException):
            await security.authenticate_user(fake_username, password)

    async def test_database_get_user(self):
        username = TEST_USERNAME
        password = TEST_PASSWORD

        self.assertTrue(await database_manager.check_username_exists(username), "Test user should exist")
        self.assertFalse(await database_manager.check_username_exists("wrong"), "Test user should not exist")

        user: UserInDB | None = await database_manager.get_user_by_username(username)
        if user is None:
            self.fail("Test user should be found by username")

        self.assertTrue(hasher.verify_password(password, user.hashed_password), "Test user should have the correct password")

        user_by_id: UserInDB | None = await database_manager.get_user_by_id(user.id)
        if user_by_id is None:
            self.fail("Test user should be found by id")

        self.assertEqual(user.id, user_by_id.id, "Test user should have the same id")
        self.assertEqual(user.username, user_by_id.username, "Test user should have the same username")
        self.assertEqual(user.hashed_password, user_by_id.hashed_password, "Test user should have the same hashed password")

    async def test_database_add_delete_user(self):
        username = f"testUser{random.randint(0, 10000)}"
        password = TEST_PASSWORD

        self.assertTrue(await database_manager.add_user(username, password), "Test user should be added")
        self.assertFalse(await database_manager.add_user(username, password), "Test user should not be added twice")
        self.assertTrue(await database_manager.check_username_exists(username), "Test user should exist")

        user: UserInDB | None = await database_manager.get_user_by_username(username)
        if user is None:
            self.fail("Test user should be found by username")

        await database_manager.delete_user(user.id)
        self.assertFalse(await database_manager.check_username_exists(username), "Test user should not exist")
        with self.assertRaises(HTTPException):
            await database_manager.delete_user(user.id)
        self.assertFalse(await database_manager.check_username_exists(username), "Test user should not exist (test of double delete)")


class TestHydroponic(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.__username = f"testUser{random.randint(0, 10000)}"
        cls.__password = TEST_PASSWORD

        is_added: bool = asyncio.run(database_manager.add_user(cls.__username, cls.__password))
        assert is_added, "Test user should be added"

        cls.__user: UserInDB | None = asyncio.run(database_manager.get_user_by_username(cls.__username))
        assert cls.__user is not None, "Test user should be found by username"

    @classmethod
    def tearDownClass(cls):
        assert cls.__user is not None, "Test user should be found by username"
        try:
            asyncio.run(database_manager.delete_user(cls.__user.id))
        except HTTPException:
            assert False, "Test user was errornous on delete"

    async def test_get_add_delete_hydroponics(self):
        if self.__user is None:
            self.fail("Test user should be found by username")

        await database_manager.add_hydroponic(TEST_HYDROPONIC, self.__user.id)
        list_of_hydroponics: list[Hydroponic] = await database_manager.get_all_hydroponics(self.__user.id)
        self.assertGreater(len(list_of_hydroponics), 0, "Test user should have at least one hydroponic - added one")

        max_id = max(tuple(hydroponic.id for hydroponic in list_of_hydroponics if hydroponic.id is not None), default=-1)
        if max_id == -1:
            self.fail("Test user should have at least one hydroponic - added one (get hydroponic id error)")

        try:
            hydroponic: Hydroponic | None = await database_manager.get_hydroponic_by_id(max_id, self.__user.id)
        except HTTPException:
            self.fail("Test user should have at least one hydroponic - added one (get hydroponic by id (1))")

        if hydroponic is None:
            self.fail("Test user should have at least one hydroponic - added one (get hydroponic by id (2))")

        self.assertEqual(hydroponic.name, TEST_HYDROPONIC.name, "Test hydroponic should have the same name as send one")
        self.assertEqual(hydroponic.water_amount, TEST_HYDROPONIC.water_amount, "Test hydroponic should have the same water amount as send one")
        self.assertEqual(hydroponic.water_consumption, TEST_HYDROPONIC.water_consumption, "Test hydroponic should have the same water consumption as send one")
        self.assertEqual(hydroponic.minerals_amount, TEST_HYDROPONIC.minerals_amount, "Test hydroponic should have the same minerals amount as send one")
        self.assertEqual(hydroponic.minerals_optimal, TEST_HYDROPONIC.minerals_optimal, "Test hydroponic should have the same minerals optimal as send one")
        self.assertEqual(hydroponic.minerals_consumption, TEST_HYDROPONIC.minerals_consumption, "Test hydroponic should have the same minerals consumption as send one")
        self.assertEqual(hydroponic.acidity_optimal_ph, TEST_HYDROPONIC.acidity_optimal_ph, "Test hydroponic should have the same acidity optimal ph as send one")
        self.assertEqual(hydroponic.temperature_C_optimal, TEST_HYDROPONIC.temperature_C_optimal, "Test hydroponic should have the same temperature optimal as send one")
        self.assertEqual(hydroponic.oxygen_amount, TEST_HYDROPONIC.oxygen_amount, "Test hydroponic should have the same oxygen amount as send one")
        self.assertEqual(hydroponic.oxygen_consumption, TEST_HYDROPONIC.oxygen_consumption, "Test hydroponic should have the same oxygen consumption as send one")

        # ---

        try:
            await database_manager.delete_hydroponic(max_id, self.__user.id)
        except HTTPException:
            self.fail("Error on deletion of hydroponic")

        self.assertIsNone(await database_manager.get_hydroponic_by_id(max_id, self.__user.id), "Test should not have hydroponic with id after it's deletion")


class TestChangeHydroponic(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.__username = f"testUser{random.randint(0, 10000)}"
        cls.__password = TEST_PASSWORD

        is_added: bool = asyncio.run(database_manager.add_user(cls.__username, cls.__password))
        assert is_added, "Test user should be added"

        cls.__user: UserInDB | None = asyncio.run(database_manager.get_user_by_username(cls.__username))
        assert cls.__user is not None, "Test user should be found by username"

        asyncio.run(database_manager.add_hydroponic(TEST_HYDROPONIC, cls.__user.id))
        list_of_hydroponics = asyncio.run(database_manager.get_all_hydroponics(cls.__user.id))
        assert len(list_of_hydroponics) > 0, "Test user should have at least one hydroponic - added one"

        max_id = max(tuple(hydroponic.id for hydroponic in list_of_hydroponics if hydroponic.id is not None), default=-1)
        assert max_id != -1, "Test user should have at least one hydroponic - added one (get hydroponic id error)"
        cls.__hydroponic_id = max_id

    @classmethod
    def tearDownClass(cls):
        assert cls.__user is not None, "Test user should be found by username"
        try:
            asyncio.run(database_manager.delete_user(cls.__user.id))
        except HTTPException:
            assert False, "Test user was errornous on delete"

    def setUp(self) -> None:
        if self.__user is None:
            self.fail("Test user should be found by username")

        self.user_id: int = self.__user.id
        if self.__hydroponic_id is None:
            self.fail("Test hydroponic should be found by id")
        hydroponic_temp = asyncio.run(database_manager.get_hydroponic_by_id(self.__hydroponic_id, self.user_id))
        if hydroponic_temp is None:
            self.fail("Test hydroponic should be found by id")
        self.hydroponic: Hydroponic = hydroponic_temp

    async def test_change_hydroponic_add_water(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.add_10_percent_water(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        add_delta = min(TEST_HYDROPONIC.water_amount - self.hydroponic.value_water, TEST_HYDROPONIC.water_amount * 0.1)

        if abs(new_hydroponic.value_water - self.hydroponic.value_water - add_delta) > 0.001:
            self.fail("Test hydroponic should have the same water amount as send one")

    async def test_change_hydroponic_add_minerals(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.add_5_percent_minerals(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        add_delta = min(TEST_HYDROPONIC.minerals_amount - self.hydroponic.minerals_amount, TEST_HYDROPONIC.minerals_amount * 0.05)

        if abs(new_hydroponic.minerals_amount - self.hydroponic.minerals_amount - add_delta) > 0.001:
            self.fail("Test hydroponic should have the same minerals amount as send one")

    async def test_change_hydroponic_add_temperature(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.add_1_celsius_temperature(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        add_delta = min(database_manager.HYDROPONIC_MAX_TEMPERATURE - self.hydroponic.value_temperature_C, 1)

        if abs(new_hydroponic.value_temperature_C - add_delta - self.hydroponic.value_temperature_C) > 0.001:
            self.fail("Test hydroponic should have the same temperature current as send one")

    async def test_change_hydroponic_lower_temperature(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.lower_1_celsius_temperature(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        lower_delta = min(self.hydroponic.value_temperature_C - database_manager.HYDROPONIC_MIN_TEMPERATURE, 1)

        if abs(self.hydroponic.value_temperature_C - lower_delta - new_hydroponic.value_temperature_C) > 0.001:
            self.fail("Test hydroponic should have the same temperature current as send one")

    async def test_change_hydroponic_add_acid(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.add_0_25_acid(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        add_delta = min(self.hydroponic.value_acidity_ph - database_manager.HYDROPONIC_MIN_PH, 0.25)
        if abs(self.hydroponic.value_acidity_ph - add_delta - new_hydroponic.value_acidity_ph) > 0.001:
            self.fail("Test hydroponic should have the same acid amount as send one")

    async def test_change_hydroponic_lower_acid(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.lower_0_25_acid(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        lower_delta = min(database_manager.HYDROPONIC_MAX_PH - self.hydroponic.value_acidity_ph, 0.25)

        if abs(self.hydroponic.value_acidity_ph + lower_delta - new_hydroponic.value_acidity_ph) > 0.001:
            self.fail("Test hydroponic should have the same acid amount as send one")

    async def test_change_hydroponic_add_oxygen(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        await database_manager.add_5_percent_oxygen(self.hydroponic.id, self.user_id)
        new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
        if new_hydroponic is None:
            self.fail("Test hydroponic should be found by id")

        add_delta = min(TEST_HYDROPONIC.oxygen_amount - self.hydroponic.oxygen_amount, TEST_HYDROPONIC.oxygen_amount * 0.05)

        if abs(self.hydroponic.oxygen_amount - add_delta - new_hydroponic.oxygen_amount) > 0.001:
            self.fail("Test hydroponic should have the same oxygen amount as send one")

    async def test_change_hydroponic_reload(self):
        if self.hydroponic.id is None:
            self.fail("Test hydroponic should be found by id")
        is_randomized = False
        for _ in range(10):
            await database_manager.reset(self.hydroponic.id, self.user_id)
            new_hydroponic = await database_manager.get_hydroponic_by_id(self.hydroponic.id, self.user_id)
            if new_hydroponic is None:
                self.fail("Test hydroponic should be found by id")

            if (
                self.hydroponic.value_temperature_C != new_hydroponic.value_temperature_C and
                self.hydroponic.value_acidity_ph != new_hydroponic.value_acidity_ph and
                self.hydroponic.value_minerals != new_hydroponic.value_minerals and
                self.hydroponic.value_oxygen != new_hydroponic.value_oxygen and
                self.hydroponic.value_water != new_hydroponic.value_water
            ):
                is_randomized = True
                break

        self.assertTrue(is_randomized, "Test hydroponic should be randomized, yet wasn't after 10 tries")


if __name__ == '__main__':
    unittest.main()
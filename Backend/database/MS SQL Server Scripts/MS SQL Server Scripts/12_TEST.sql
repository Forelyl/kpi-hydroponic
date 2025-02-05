USE Hydroponic;
GO

---

EXEC tSQLt.NewTestClass 'testHydroponic';
GO

---------------------------------------------------------------
-- Test for valid situations

CREATE OR ALTER PROCEDURE testHydroponic.test_valid_insert_delete_user
    AS
BEGIN
    DECLARE @initial INT;
    DECLARE @final INT;
    DECLARE @count INT;

    SET @initial = (SELECT COUNT(*) FROM [user]);
    SET @final = @initial + 1;

    INSERT INTO [user] (username, hash_salt) VALUES ('valid_user', 'some_hash');
    SET @count = (SELECT COUNT(*) FROM [user]);
    IF @count != @final
        EXEC tSQLt.Fail 'Row was not inserted';

    DELETE FROM [user] WHERE username = 'valid_user';
    SET @count = (SELECT COUNT(*) FROM [user]);
    IF @count != @initial
        EXEC tSQLt.Fail 'Row was not deleted';
END;
GO


CREATE OR ALTER PROCEDURE testHydroponic.test_valid_update_user
    AS
BEGIN
    INSERT INTO [user] (username, hash_salt) VALUES ('valid_user', 'some_hash');

    UPDATE [user] SET hash_salt = 'new_hash' WHERE username = 'valid_user';

    DECLARE @actual NVARCHAR(255);
    SET @actual = (SELECT hash_salt FROM [user] WHERE username = 'valid_user');
    EXEC tSQLt.AssertEquals 'new_hash', @actual, 'Row was not updated';

    DELETE FROM [user] WHERE username = 'valid_user';
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_valid_insert_delete_hydroponic
    AS
BEGIN
    DECLARE @inserted INT;
    DECLARE @count INT;
    DECLARE @initial INT;
    DECLARE @final INT;

    SET @initial = (SELECT COUNT(*) FROM hydroponic);
    SET @final = @initial + 1;

    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'System1', 10.0, 1, 5.0, 1, 1, 7.0, 20.0, 2.0, 1, 1.0, 2.0, 6.5, 15.0, 1.5);
    SET @count = (SELECT COUNT(*) FROM hydroponic);
    EXEC tSQLt.AssertEquals @final, @count, 'Row was not inserted';

    DELETE FROM hydroponic WHERE [name] = 'System1';
    SET @count = (SELECT COUNT(*) FROM hydroponic);
    EXEC tSQLt.AssertEquals @initial, @count, 'Row was not deleted';

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_valid_update_hydroponic
    AS
BEGIN
    DECLARE @actual FLOAT;
    DECLARE @inserted INT;

    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'System1', 10.0, 1, 5.0, 1, 1, 7.0, 20.0, 2.0, 1, 1.0, 2.0, 6.5, 15.0, 1.5);

    UPDATE hydroponic SET value_water = 10 WHERE [name] = 'System1';
    SET @actual = (SELECT value_water FROM hydroponic WHERE [name] = 'System1');
    IF ABS(@actual - 10) > 0.000001
        EXEC tSQLt.Fail 'Row was not updated (1)';

    UPDATE hydroponic SET value_minerals = 3.1 WHERE [name] = 'System1';
    SET @actual = (SELECT value_minerals FROM hydroponic WHERE [name] = 'System1');
    IF ABS(@actual - 3.1) > 0.000001
        EXEC tSQLt.Fail 'Row was not updated (2)';

    UPDATE hydroponic SET value_acidity_ph = 7.2 WHERE [name] = 'System1';
    SET @actual = (SELECT value_acidity_ph FROM hydroponic WHERE [name] = 'System1');
    IF ABS(@actual - 7.2) > 0.000001
        EXEC tSQLt.Fail 'Row was not updated (3)';

    UPDATE hydroponic SET value_temperature_C = 20 WHERE [name] = 'System1';
    SET @actual = (SELECT value_temperature_C FROM hydroponic WHERE [name] = 'System1');
    IF ABS(@actual - 20) > 0.000001
        EXEC tSQLt.Fail 'Row was not updated (4)';

    UPDATE hydroponic SET value_oxygen = 0 WHERE [name] = 'System1';
    SET @actual = (SELECT value_oxygen FROM hydroponic WHERE [name] = 'System1');
    IF ABS(@actual - 0) > 0.000001
        EXEC tSQLt.Fail 'Row was not updated (5)';

    DELETE FROM hydroponic WHERE [name] = 'System1';
    DELETE FROM [user] WHERE id = @inserted;

END;
GO


CREATE OR ALTER PROCEDURE testHydroponic.test_valid_delete_cascade_hydroponic
    AS
BEGIN
    DECLARE @count INT;
    DECLARE @initial INT;
    DECLARE @final INT;
    DECLARE @inserted INT;

    SET @initial = (SELECT COUNT(*) FROM hydroponic);
    SET @final = @initial + 1;

    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'System1', 10.0, 1, 5.0, 1, 1, 7.0, 20.0, 2.0, 1, 1.0, 2.0, 6.5, 15.0, 1.5);

    SET @count = (SELECT COUNT(*) FROM hydroponic);
    EXEC tSQLt.AssertEquals @final, @count, 'Row was not inserted';

    DELETE FROM [user] WHERE username = 'owner';
    SET @count = (SELECT COUNT(*) FROM hydroponic);
    EXEC tSQLt.AssertEquals @initial, @count, 'Row was not deleted on cascade delete';
END;
GO

---------------------------------------------------------------
-- Test for invalid situations

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_user_name_collision
    AS
BEGIN
    INSERT INTO [user] (username, hash_salt) VALUES ('duplicate_user', 'some_salt');

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 2627;
    INSERT INTO [user] (username, hash_salt) VALUES ('duplicate_user', 'another_salt');

    DELETE FROM [user] WHERE username = 'duplicate_user';
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_user_null_username
    AS
BEGIN
    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 515;
    INSERT INTO [user] (username, hash_salt) VALUES (NULL, 'some_salt');
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_user_null_hash_salt
    AS
BEGIN
    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 515;
    INSERT INTO [user] (username, hash_salt) VALUES ('user_with_null_salt', NULL);
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_negative_water_amount
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'NegativeWaterSystem', -10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);
    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_trigger_value_water_exceeds_limit
    AS
BEGIN
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    DECLARE @inserted INT = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 50001;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'InvalidSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 15.0, 2.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_null_user_id_owner
    AS
BEGIN
    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 515;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (NULL, 'NoOwnerSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_acidity_ph_out_of_range
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'AciditySystem', 10.0, 1.0, 5.0, 1.0, 1.0, 20.0, 20.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO


CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_trigger_value_oxygen_exceeds_limit
    AS
BEGIN
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    DECLARE @inserted INT = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 50001;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'InvalidOxygenSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 10.0);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_trigger_value_minerals_exceeds_limit
    AS
BEGIN
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    DECLARE @inserted INT = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 50001;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'InvalidMineralSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 10.0, 12.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_temperature_C_optimal_out_of_range
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'TemperatureSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 50.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_value_temperature_C_out_of_range
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'LowTemperatureSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, 2.0, 1.0, 1.0, 2.0, 4.0, 1.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_oxygen_amount_non_positive
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'NoOxygenSystem', 10.0, 1.0, 5.0, 1.0, 1.0, 7.0, 20.0, -1.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO

CREATE OR ALTER PROCEDURE testHydroponic.test_invalid_hydroponic_acidity_optimal_ph_out_of_range
    AS
BEGIN
    DECLARE @inserted INT;
    INSERT INTO [user] (username, hash_salt) VALUES ('owner', 'some_salt');
    SET @inserted = SCOPE_IDENTITY();

    EXEC tSQLt.ExpectException @ExpectedErrorNumber = 547;
    INSERT INTO hydroponic (
        user_id_owner, [name], water_amount, water_consumption, minerals_amount, minerals_optimal, minerals_consumption,
        acidity_optimal_ph, temperature_C_optimal, oxygen_amount, oxygen_consumption, value_water, value_minerals,
        value_acidity_ph, value_temperature_C, value_oxygen
    )
    VALUES (@inserted, 'InvalidAciditySystem', 10.0, 1.0, 5.0, 1.0, 1.0, 45.0, 20.0, 2.0, 1.0, 1.0, 2.0, 6.5, 15.0, 1.5);

    DELETE FROM [user] WHERE id = @inserted;
END;
GO
---------------------------------------------------------------

EXEC tSQLt.Run 'testHydroponic'
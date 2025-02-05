USE Hydroponic;
GO


CREATE OR ALTER TRIGGER trg_hydroponic_insert_update_checks
ON hydroponic
AFTER INSERT, UPDATE
	AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE value_water > water_amount)
    BEGIN
        THROW 50001, 'value_water exceeds the allowed (declared by water_amount) limits', 1;
    END
	IF EXISTS (SELECT 1 FROM inserted WHERE value_minerals > minerals_amount)
    BEGIN
        THROW 50001, 'value_minerals exceeds the allowed (declared by minerals_amount) limits', 1;
    END
	IF EXISTS (SELECT 1 FROM inserted WHERE value_oxygen > oxygen_amount)
    BEGIN
        THROW 50001, 'value_oxygen exceeds the allowed (declared by oxygen_amount) limits', 1;
    END
END;
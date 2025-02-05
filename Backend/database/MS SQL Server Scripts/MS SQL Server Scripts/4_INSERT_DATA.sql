use Hydroponic;
GO

-- hashed password is - "secret" (the value not a secret), in all cases
INSERT INTO "user" (username, hash_salt)
VALUES 
    ('Mia',       '$argon2id$v=19$m=65536,t=3,p=4$cQ4BYCzFGKOUck4JIaRUyg$vO9D8BSRv/CCN5xNrd1W1fsvoW14VI8yZEoXMDTJOE8'),
    ('Talli',     '$argon2id$v=19$m=65536,t=3,p=4$sXYO4TxnLIVQai1FSAmhdA$Xlk/ynjr2VpX2Q7vf1PxUFHu8USArfh6NSsXc+yrK/0'),
    ('Harengard', '$argon2id$v=19$m=65536,t=3,p=4$8H7PmTNmDEHoHeO811orhQ$uXaKplwDSu8vkjyApWVKU0uI1B2YOyJlFpU8lYYoIiE');


INSERT INTO hydroponic (
    user_id_owner, "name", water_amount, water_consumption,
    minerals_amount, minerals_optimal, minerals_consumption,
    acidity_optimal_ph, temperature_C_optimal, 
	oxygen_amount, oxygen_consumption,
	value_water, value_minerals, value_acidity_ph, value_temperature_C, value_oxygen
)
VALUES
    (1, 'Plant System 1', 1000.0, 10,     50.0, 30, 2,       6.5, 20.0,     50.0, 0.5,      500, 25, 5.5, 18, 30),
    (2, 'Plant System 2', 1500.0, 17,     60.0, 40, 3,       7.0, 22.0,     62.0, 0.5,      750, 25, 5.5, 18, 30),
    (3, 'Plant System 3', 1200.0, 16,     55.0, 42, 2.5,     6.8, 21.0,     71.0, 0.5,      600, 25, 5.5, 18, 30);

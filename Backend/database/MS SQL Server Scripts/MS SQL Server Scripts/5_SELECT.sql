USE Hydroponic;
GO

SELECT * FROM "user";
SELECT * FROM hydroponic;


SELECT 
    u.id AS user_id, 
    u.username, 
    h."name" AS hydroponic_name, 
    h.water_amount, 
    h.temperature_C_optimal 
FROM 
    "user" u
LEFT JOIN 
    hydroponic h
ON 
    u.id = h.user_id_owner;
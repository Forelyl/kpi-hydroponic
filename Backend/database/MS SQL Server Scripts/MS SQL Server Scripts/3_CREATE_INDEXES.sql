USE Hydroponic;
GO

-- No need in index cause column is already unique (by this it already has an index)
-- CREATE UNIQUE INDEX IX_USER_USERNAME ON "user"(username);
-- GO

CREATE NONCLUSTERED INDEX IX_HYDROPONIC_USER_ID_OWNER
ON hydroponic (user_id_owner);
GO
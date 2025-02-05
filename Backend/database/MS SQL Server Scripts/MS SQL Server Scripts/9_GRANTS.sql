USE Hydroponic;
GO

-- Grant SELECT, INSERT, UPDATE, DELETE on the "user" table
GRANT SELECT, INSERT, UPDATE, DELETE ON "user" TO "hydroponic-vsrhjvzrj";

-- Grant SELECT, INSERT, UPDATE, DELETE on the "hydroponic" table
GRANT SELECT, INSERT, UPDATE, DELETE ON hydroponic TO "hydroponic-vsrhjvzrj";

-- Optional: Grant REFERENCES if user needs to create foreign keys referencing these tables
GRANT REFERENCES ON "user" TO "hydroponic-vsrhjvzrj";
GRANT REFERENCES ON hydroponic TO "hydroponic-vsrhjvzrj";
USE Hydroponic;
GO

CREATE TABLE "user" (
	id	      INT IDENTITY(1, 1)  PRIMARY KEY,
	username  NVARCHAR(255) NOT NULL UNIQUE,
	hash_salt NVARCHAR(255) NOT NULL
);

CREATE TABLE hydroponic (
	id							INT IDENTITY(1, 1) PRIMARY KEY,
	user_id_owner				INT NOT NULL,

	"name"						NVARCHAR(255) NOT NULL,
	
	water_amount				FLOAT NOT NULL CHECK (water_amount > 0),
	water_consumption			FLOAT NOT NULL CHECK (water_consumption > 0),
	
	minerals_amount				FLOAT NOT NULL CHECK (minerals_amount      > 0),
	minerals_optimal			FLOAT NOT NULL CHECK (minerals_optimal     > 0),
	minerals_consumption		FLOAT NOT NULL CHECK (minerals_consumption > 0),

	acidity_optimal_ph			FLOAT NOT NULL CHECK (acidity_optimal_ph        >= 0 AND acidity_optimal_ph        <= 14),
	temperature_C_optimal		FLOAT NOT NULL CHECK (temperature_C_optimal     >= 5 AND temperature_C_optimal     <= 25),
	
	oxygen_amount				FLOAT NOT NULL CHECK (oxygen_amount      > 0),
	oxygen_consumption  		FLOAT NOT NULL CHECK (oxygen_consumption > 0),
	--

	value_water					FLOAT NOT NULL CHECK (value_water             >= 0),
	value_minerals				FLOAT NOT NULL CHECK (value_minerals          >= 0),
	value_acidity_ph			FLOAT NOT NULL CHECK (value_acidity_ph        >= 0 AND value_acidity_ph        <= 14),
	value_temperature_C			FLOAT NOT NULL CHECK (value_temperature_C     >= 5 AND value_temperature_C     <= 25),
	value_oxygen              	FLOAT NOT NULL CHECK (value_oxygen            >= 0),

	FOREIGN KEY (user_id_owner) REFERENCES "user"(id) ON DELETE CASCADE
);
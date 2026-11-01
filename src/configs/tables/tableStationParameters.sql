CREATE TABLE stationParameters (
    dataSource varchar(255) NOT NULL,
    stationId varchar(255) NOT NULL,
    parameterId varchar(255) NOT NULL,
    PRIMARY KEY (dataSource, stationId, parameterId)
);

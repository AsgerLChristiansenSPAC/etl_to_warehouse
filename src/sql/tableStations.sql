CREATE TABLE stations (
    dataSource varchar(255) NOT NULL,
    stationId varchar(255) NOT NULL,
    validFrom varchar(255) NOT NULL,
    validTo varchar(255),
    PRIMARY KEY (dataSource, stationId, validFrom)
);
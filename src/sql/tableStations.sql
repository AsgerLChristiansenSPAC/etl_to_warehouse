CREATE TABLE stations (
    dataSource varchar(255) NOT NULL,
    stationId varchar(255) NOT NULL,
    PRIMARY KEY (dataSource, stationId)
);
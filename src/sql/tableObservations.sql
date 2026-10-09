CREATE TABLE observations (
    dataSource varchar(255) NOT NULL,
    stationId varchar(255) NOT NULL,
    parameterId varchar(255) NOT NULL,
    calculatedAt varchar(255) NOT NULL,
    observationValue FLOAT,
    observationUnit varchar(255),
    PRIMARY KEY (dataSource, stationId, parameterId, calculatedAt)
);
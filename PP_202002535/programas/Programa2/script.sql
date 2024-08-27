create database combustible;
use combustible;

create table tipo_combustible (
	id int auto_increment primary key,
    nombre varchar(50) not null,
    precio decimal(10, 2) not null
);

INSERT INTO tipo_combustible (nombre, precio) VALUES
('Gasolina Regular', 4.50),
('Gasolina Premium', 5.00),
('Diesel', 3.80);

select * from tipo_combustible;
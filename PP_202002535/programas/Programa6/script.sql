create database combustible;
use combustible;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    placa VARCHAR(50) NOT NULL
);

create table tipo_combustible (
	id int auto_increment primary key,
    nombre varchar(50) not null,
    precio decimal(10, 2) not null
);

INSERT INTO tipo_combustible (nombre, precio) VALUES
('Gasolina Regular', 4.50),
('Gasolina Premium', 5.00),
('Diesel', 3.80)
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), precio=VALUES(precio);

select * from tipo_combustible;
drop table clientes;
drop table tipo_combustible;
drop database combustible;
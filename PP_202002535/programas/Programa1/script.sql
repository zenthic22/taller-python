create database cliente_vehiculo;
use cliente_vehiculo;

create table Cliente (
	id int auto_increment primary key,
    nombre_cliente varchar(50) not null,
    placa varchar(50) not null
);

select * from Cliente;
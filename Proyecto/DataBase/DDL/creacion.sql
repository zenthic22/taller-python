create database db_proyecto;
use db_proyecto;

CREATE TABLE `Rol` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL
);

CREATE TABLE `Usuario` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `DPI` VARCHAR(13) NOT NULL,
  `fecha_nacimiento` DATE,
  `telefono` VARCHAR(15),
  `nombre_usuario` VARCHAR(50) UNIQUE NOT NULL,
  `email` VARCHAR(100),
  `password` VARCHAR(255) NOT NULL,
  `rol_id` INT NOT NULL
);

ALTER TABLE `Usuario` ADD FOREIGN KEY (`rol_id`) REFERENCES `Rol` (`id`);

drop database db_proyecto;
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
  `password` VARCHAR(255) NOT NULL,
  `rol_id` INT,
  `login_attempts` INT DEFAULT 0,
  `account_locked` BOOLEAN DEFAULT false,
  `reconocimiento_facial` BOOLEAN DEFAULT false
);

CREATE TABLE `Estudiante` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` INT,
  `fecha_nacimiento` DATE,
  `telefono` VARCHAR(15),
  `nombre_usuario` VARCHAR(50) UNIQUE,
  `email` VARCHAR(100)
);

CREATE TABLE `Catedratico` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` INT,
  `especialidad` VARCHAR(100)
);

CREATE TABLE `Curso` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `codigo` VARCHAR(10) UNIQUE NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `horario` VARCHAR(100),
  `cupo` INT NOT NULL,
  `catedratico_id` INT,
  `banner` VARCHAR(255),
  `mensaje_bienvenida` TEXT,
  `estado` BOOLEAN DEFAULT true
);

CREATE TABLE `Inscripcion` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` INT,
  `curso_id` INT,
  `fecha_inscripcion` DATE NOT NULL
);

CREATE TABLE `RestablecerPassword` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` INT,
  `token` VARCHAR(255) NOT NULL,
  `expiracion` DATETIME NOT NULL
);

CREATE TABLE `HistorialInscripciones` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `inscripcion_id` INT,
  `fecha_modificacion` DATE NOT NULL,
  `estado` VARCHAR(20)
);

CREATE TABLE `Nota` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `inscripcion_id` INT,
  `nota` DECIMAL(5,2)
);

CREATE TABLE `Certificado` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `inscripcion_id` INT,
  `fecha_emision` DATE NOT NULL
);

ALTER TABLE `Usuario` ADD FOREIGN KEY (`rol_id`) REFERENCES `Rol` (`id`);

ALTER TABLE `Estudiante` ADD FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`);

ALTER TABLE `Catedratico` ADD FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`);

ALTER TABLE `Curso` ADD FOREIGN KEY (`catedratico_id`) REFERENCES `Catedratico` (`id`);

ALTER TABLE `Inscripcion` ADD FOREIGN KEY (`usuario_id`) REFERENCES `Estudiante` (`usuario_id`);

ALTER TABLE `Inscripcion` ADD FOREIGN KEY (`curso_id`) REFERENCES `Curso` (`id`);

ALTER TABLE `RestablecerPassword` ADD FOREIGN KEY (`usuario_id`) REFERENCES `Usuario` (`id`);

ALTER TABLE `HistorialInscripciones` ADD FOREIGN KEY (`inscripcion_id`) REFERENCES `Inscripcion` (`id`);

ALTER TABLE `Nota` ADD FOREIGN KEY (`inscripcion_id`) REFERENCES `Inscripcion` (`id`);

ALTER TABLE `Certificado` ADD FOREIGN KEY (`inscripcion_id`) REFERENCES `Inscripcion` (`id`);

drop database db_proyecto;
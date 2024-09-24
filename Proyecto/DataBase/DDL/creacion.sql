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
  `nombre_usuario` VARCHAR(50) UNIQUE,
  `email` VARCHAR(100),
  `password` VARCHAR(255) NOT NULL,
  `rol_id` INT NOT NULL
);

CREATE TABLE `Curso` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `codigo` VARCHAR(10) UNIQUE NOT NULL,
  `costo` DECIMAL(10, 2) NOT NULL,
  `horario` VARCHAR(100),
  `cupo` INT NOT NULL,
  `catedratico_id` INT,
  `banner` VARCHAR(255),  -- Ruta de imagen para el banner
  `mensaje_bienvenida` TEXT,  -- Mensaje de bienvenida del catedrático
  FOREIGN KEY (`catedratico_id`) REFERENCES `Usuario`(`id`)
    ON DELETE SET NULL
);

CREATE TABLE `Inscripcion` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `curso_id` INT NOT NULL,
  `fecha_inscripcion` DATE NOT NULL,
  FOREIGN KEY (`usuario_id`) REFERENCES `Usuario`(`id`),
  FOREIGN KEY (`curso_id`) REFERENCES `Curso`(`id`)
);

ALTER TABLE `Usuario` ADD FOREIGN KEY (`rol_id`) REFERENCES `Rol` (`id`);
ALTER TABLE `Usuario`
ADD COLUMN `login_attempts` INT DEFAULT 0,
ADD COLUMN `account_locked` BOOLEAN DEFAULT FALSE;

drop database db_proyecto;
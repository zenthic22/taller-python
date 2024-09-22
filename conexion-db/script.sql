/*creamos una base de datos*/
create database db_cursos;
/*empezaremos a utilizarla*/
use db_cursos;
/*crearemos una tabla en este caso seran los cursos de la universidad*/
create table cursos (
	codigo smallint, /*smallint es un tipo de dato entero pero recibe menor cantidad de bytes*/
    nombre varchar(50), /*varchar es un tipo de dato tipo caracter variable, es decir puede establecer un tamaño que es lo mismo que decir un string*/
    creditos smallint
);
/*ahora procederemos a visualizar los datos, por defecto no se vera ninguno ya que no se ha realizado una insercion*/
select * from cursos;

/*ahora realizaremos una insercion de datos*/
insert into cursos values(0777, 'Organizacion de Lenguajes y Compiladores 1', 4);
insert into cursos values(0281, 'Sistemas Operativos 1', 4);
insert into cursos values(0283, 'Analisis y Diseño 1', 5);
insert into cursos values(0285, 'Sistemas Operativos 2', 5);

/*actualizaremos el estado de la tabla*/
select * from cursos;

/*eliminaremos una columna en especifico*/
delete from cursos where codigo = 0777;

/*eliminaremos todas las columnas de la tabla*/
delete from cursos;

/*actualizaremos una columna en especifico*/
/*desactivamos el modo seguro esto lo haremos para poder actualizar*/
set SQL_SAFE_UPDATES = 0;
/*realizamos la actualizacion*/
update cursos set nombre = 'AYD 1' where codigo = 0283;

/*eliminaremos toda la tabla*/
drop table cursos;

/*eliminar base de datos*/
drop database db_cursos;
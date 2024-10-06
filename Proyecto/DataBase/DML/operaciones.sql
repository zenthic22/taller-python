insert into rol (id, nombre) values
(1, 'Administrador'),
(2, 'Catedrático'),
(3, 'Estudiante');

select * from usuario;
select * from estudiante;
select * from catedratico;
select * from curso;
select * from rol;

SELECT 
                u.nombre AS catedratico_nombre,
                u.apellido AS catedratico_apellido,
                u.DPI AS catedratico_dpi,
                c.especialidad AS catedratico_especialidad,
                cu.nombre AS curso_nombre,
                cu.codigo AS curso_codigo,
                cu.horario AS curso_horario,
                cu.costo AS curso_costo,
                cu.cupo AS curso_cupo
            FROM Catedratico c
            JOIN Usuario u ON c.usuario_id = u.id
            LEFT JOIN Curso cu ON cu.catedratico_id = c.id
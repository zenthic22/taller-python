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
LEFT JOIN Curso cu ON cu.catedratico_id = c.id;

SELECT c.id, c.nombre, c.banner 
FROM Curso c
JOIN Catedratico ca ON c.catedratico_id = ca.id
JOIN Usuario u ON ca.usuario_id = u.id
WHERE u.id = 2;  -- Reemplaza ? con el ID de usuario del catedrático que deseas consultar.

SELECT c.id, c.nombre, c.banner, c.descripcion, c.horario 
FROM Curso c
JOIN Catedratico ca ON c.catedratico_id = ca.id
JOIN Usuario u ON ca.usuario_id = u.id
WHERE u.id = 2;

SELECT id, nombre, estado, cupo FROM Curso WHERE estado = 1;

SELECT id, nombre_usuario, email FROM Estudiante;

SELECT i.id, i.usuario_id, i.curso_id, i.fecha_inscripcion 
FROM Inscripcion i 
JOIN Estudiante e ON i.usuario_id = e.usuario_id 
JOIN Curso c ON i.curso_id = c.id;

SELECT c.id, c.nombre, c.cupo, c.estado 
FROM Curso c 
WHERE c.id = 2;

SELECT * FROM Inscripcion WHERE usuario_id = 6 AND curso_id = 1;
select * from nota;

SELECT n.nota
FROM Nota n
JOIN Inscripcion i ON n.inscripcion_id = i.id
WHERE i.usuario_id = 6 AND i.curso_id = 1;

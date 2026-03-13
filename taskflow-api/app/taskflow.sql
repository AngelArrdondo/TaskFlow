-- ===================================================
-- TASKFLOW API - BASE DE DATOS COMPLETA
-- CON TUS DATOS EXACTOS DE phpMyAdmin
-- ===================================================

-- Eliminar base de datos si existe (¡CUIDADO! Esto borrará todo)
-- DROP DATABASE IF EXISTS taskflow_db;

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS taskflow_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE taskflow_db;

-- ===================================================
-- TABLA: etiquetas
-- ===================================================
CREATE TABLE IF NOT EXISTS etiquetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===================================================
-- TABLA: tareas
-- ===================================================
CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300),
    fecha_limite DATE,
    completada BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_completada (completada),
    INDEX idx_fecha_limite (fecha_limite)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===================================================
-- TABLA INTERMEDIA: tarea_etiqueta
-- ===================================================
CREATE TABLE IF NOT EXISTS tarea_etiqueta (
    tarea_id INT NOT NULL,
    etiqueta_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tarea_id, etiqueta_id),
    FOREIGN KEY (tarea_id) REFERENCES tareas(id) ON DELETE CASCADE,
    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id) ON DELETE CASCADE,
    INDEX idx_tarea (tarea_id),
    INDEX idx_etiqueta (etiqueta_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===================================================
-- INSERTAR DATOS DE etiquetas (TUS 10 ETIQUETAS EXACTAS)
-- ===================================================
INSERT INTO etiquetas (id, nombre, created_at) VALUES
(1, 'Urgente', '2026-03-05 22:31:14'),
(2, 'Estudio', '2026-03-05 22:31:14'),
(3, 'Alta prioridad', '2026-03-05 22:32:07'),
(4, 'Media prioridad', '2026-03-05 22:32:07'),
(5, 'Baja prioridad', '2026-03-05 22:32:07'),
(6, 'Trabajo', '2026-03-05 22:32:07'),
(7, 'Personal', '2026-03-05 22:32:07'),
(8, 'Hogar', '2026-03-05 22:32:07'),
(9, 'Salud', '2026-03-05 22:32:07'),
(10, 'Finanzas', '2026-03-05 22:32:07')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ===================================================
-- INSERTAR DATOS DE tareas (TUS 16 TAREAS EXACTAS)
-- ===================================================
INSERT INTO tareas (id, titulo, descripcion, fecha_limite, completada, created_at, updated_at) VALUES
(1, 'Estudiar FastAPI', 'Revisar documentación', '2026-03-15', 0, '2026-03-05 22:31:14', '2026-03-05 22:31:14'),
(2, 'Terminar proyecto de FastAPI', 'Completar todos los endpoints y probar con Postman', '2026-03-20', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(3, 'Estudiar para examen de AWS', 'Repasar servicios de computación y almacenamiento', '2026-03-25', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(4, 'Leer documentación de MySQL', 'Índices, joins y optimización de consultas', '2026-03-12', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(5, 'Practicar ejercicios de Python', 'Resolución de problemas en HackerRank', '2026-03-15', 1, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(6, 'Ver tutorial de Docker', 'Contenerizar aplicación de FastAPI', '2026-03-18', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(7, 'Preparar presentación semanal', 'Slides del avance del proyecto', '2026-03-09', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(8, 'Revisar pull requests', 'Revisar código de compañeros en GitHub', '2026-03-08', 1, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(9, 'Actualizar documentación', 'README y wikis del proyecto', '2026-03-11', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(10, 'Reunión con el equipo', 'Sprint planning a las 10:00 AM', '2026-03-07', 1, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(11, 'Pagar servicios', 'Luz, agua e internet', '2026-03-10', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(12, 'Cita médica', 'Chequeo anual con el doctor', '2026-03-14', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(13, 'Comprar regalo cumpleaños', 'Para mi hermano, le gusta la tecnología', '2026-03-17', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(14, 'Limpieza general', 'Ordenar habitación y escritorio', '2026-03-06', 1, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(15, 'Hacer ejercicio', '30 minutos de cardio y pesas', '2026-03-09', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40'),
(16, 'Llamar a familia', 'Hablar con padres y abuelos', '2026-03-13', 0, '2026-03-05 22:32:40', '2026-03-05 22:32:40')
ON DUPLICATE KEY UPDATE 
    titulo=VALUES(titulo),
    descripcion=VALUES(descripcion),
    fecha_limite=VALUES(fecha_limite),
    completada=VALUES(completada);

-- ===================================================
-- INSERTAR RELACIONES tarea_etiqueta (TUS 20 RELACIONES EXACTAS)
-- ===================================================
INSERT INTO tarea_etiqueta (tarea_id, etiqueta_id, created_at) VALUES
(1, 1, NOW()),  -- Tarea 1 (FastAPI) -> Urgente
(1, 2, NOW()),  -- Tarea 1 (FastAPI) -> Estudio
(2, 3, NOW()),  -- Tarea 2 (Terminar proyecto) -> Alta prioridad
(2, 6, NOW()),  -- Tarea 2 (Terminar proyecto) -> Trabajo
(3, 2, NOW()),  -- Tarea 3 (Examen AWS) -> Estudio
(3, 4, NOW()),  -- Tarea 3 (Examen AWS) -> Media prioridad
(5, 2, NOW()),  -- Tarea 5 (Python) -> Estudio
(5, 5, NOW()),  -- Tarea 5 (Python) -> Baja prioridad
(8, 6, NOW()),  -- Tarea 8 (Pull requests) -> Trabajo
(10, 1, NOW()), -- Tarea 10 (Reunión) -> Urgente
(10, 6, NOW()), -- Tarea 10 (Reunión) -> Trabajo
(11, 7, NOW()), -- Tarea 11 (Pagar servicios) -> Personal
(11, 10, NOW()), -- Tarea 11 (Pagar servicios) -> Finanzas
(12, 7, NOW()), -- Tarea 12 (Cita médica) -> Personal
(12, 9, NOW()), -- Tarea 12 (Cita médica) -> Salud
(13, 7, NOW()), -- Tarea 13 (Regalo) -> Personal
(14, 8, NOW()), -- Tarea 14 (Limpieza) -> Hogar
(15, 7, NOW()), -- Tarea 15 (Ejercicio) -> Personal
(15, 9, NOW()), -- Tarea 15 (Ejercicio) -> Salud
(16, 7, NOW())  -- Tarea 16 (Llamar familia) -> Personal
ON DUPLICATE KEY UPDATE tarea_id=VALUES(tarea_id);

-- ===================================================
-- VERIFICAR LOS DATOS INSERTADOS
-- ===================================================

-- Verificar etiquetas
SELECT 'ETIQUETAS' as 'TABLA', COUNT(*) as 'TOTAL' FROM etiquetas
UNION ALL
SELECT 'TAREAS', COUNT(*) FROM tareas
UNION ALL
SELECT 'RELACIONES', COUNT(*) FROM tarea_etiqueta;

-- Mostrar todas las tareas con sus etiquetas
SELECT 
    t.id,
    t.titulo,
    t.completada,
    GROUP_CONCAT(e.nombre ORDER BY e.nombre SEPARATOR ', ') as etiquetas
FROM tareas t
LEFT JOIN tarea_etiqueta te ON t.id = te.tarea_id
LEFT JOIN etiquetas e ON te.etiqueta_id = e.id
GROUP BY t.id
ORDER BY t.id;
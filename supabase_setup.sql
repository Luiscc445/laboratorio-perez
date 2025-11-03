-- ============================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS - LABORATORIO PÉREZ
-- Supabase PostgreSQL
-- ============================================================
-- IMPORTANTE: Ejecuta este script en Supabase SQL Editor
-- Luego ejecuta el script Python create_admin.py para crear el usuario admin

-- ============================================================
-- PASO 1: ELIMINAR TABLAS EXISTENTES (SI EXISTEN)
-- ============================================================

-- Eliminar tablas en orden correcto (por las foreign keys)
DROP TABLE IF EXISTS resultados CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;
DROP TABLE IF EXISTS pruebas CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- ============================================================
-- PASO 2: CREAR TABLA DE USUARIOS
-- ============================================================

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_is_admin ON usuarios(is_admin);

-- Comentarios de documentación
COMMENT ON TABLE usuarios IS 'Usuarios del sistema administrativo';
COMMENT ON COLUMN usuarios.username IS 'Nombre de usuario único';
COMMENT ON COLUMN usuarios.password_hash IS 'Hash de contraseña (pbkdf2:sha256)';
COMMENT ON COLUMN usuarios.is_admin IS 'Indica si el usuario es administrador';

-- ============================================================
-- PASO 3: CREAR TABLA DE PACIENTES
-- ============================================================

CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    ci VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(120),
    fecha_registro TIMESTAMP DEFAULT NOW()
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_pacientes_ci ON pacientes(ci);
CREATE INDEX idx_pacientes_nombre ON pacientes(nombre);
CREATE INDEX idx_pacientes_fecha_registro ON pacientes(fecha_registro DESC);

-- Comentarios de documentación
COMMENT ON TABLE pacientes IS 'Información de pacientes del laboratorio';
COMMENT ON COLUMN pacientes.ci IS 'Cédula de Identidad (único)';

-- ============================================================
-- PASO 4: CREAR TABLA DE RESULTADOS
-- ============================================================

CREATE TABLE resultados (
    id SERIAL PRIMARY KEY,
    numero_orden VARCHAR(50) UNIQUE NOT NULL,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE SET NULL,
    paciente_nombre VARCHAR(200) NOT NULL,
    paciente_ci VARCHAR(20) NOT NULL,
    fecha_muestra DATE,
    archivo_pdf VARCHAR(200),
    codigo_acceso VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_resultados_numero_orden ON resultados(numero_orden);
CREATE INDEX idx_resultados_paciente_id ON resultados(paciente_id);
CREATE INDEX idx_resultados_paciente_ci ON resultados(paciente_ci);
CREATE INDEX idx_resultados_codigo_acceso ON resultados(codigo_acceso);
CREATE INDEX idx_resultados_fecha_muestra ON resultados(fecha_muestra DESC);
CREATE INDEX idx_resultados_fecha_creacion ON resultados(fecha_creacion DESC);

-- Comentarios de documentación
COMMENT ON TABLE resultados IS 'Resultados de laboratorio de los pacientes';
COMMENT ON COLUMN resultados.numero_orden IS 'Número de orden único del resultado';
COMMENT ON COLUMN resultados.codigo_acceso IS 'Código para consulta pública del resultado';

-- ============================================================
-- PASO 5: CREAR TABLA DE PRUEBAS
-- ============================================================

CREATE TABLE pruebas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    descripcion TEXT,
    precio NUMERIC(10, 2) DEFAULT 0.0,
    imagen VARCHAR(200),
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_pruebas_nombre ON pruebas(nombre);
CREATE INDEX idx_pruebas_categoria ON pruebas(categoria);
CREATE INDEX idx_pruebas_fecha_creacion ON pruebas(fecha_creacion DESC);

-- Comentarios de documentación
COMMENT ON TABLE pruebas IS 'Catálogo de pruebas de laboratorio disponibles';
COMMENT ON COLUMN pruebas.precio IS 'Precio en Bolivianos (Bs)';

-- ============================================================
-- PASO 6: VERIFICAR CREACIÓN DE TABLAS
-- ============================================================

-- Listar todas las tablas creadas
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as num_columns
FROM information_schema.tables t
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    AND table_name IN ('usuarios', 'pacientes', 'resultados', 'pruebas')
ORDER BY table_name;

-- Verificar que las tablas están vacías
SELECT 'usuarios' as tabla, COUNT(*) as registros FROM usuarios
UNION ALL
SELECT 'pacientes', COUNT(*) FROM pacientes
UNION ALL
SELECT 'resultados', COUNT(*) FROM resultados
UNION ALL
SELECT 'pruebas', COUNT(*) FROM pruebas;

-- ============================================================
-- PASO 7: DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================

-- Insertar algunas pruebas de ejemplo en el catálogo
INSERT INTO pruebas (nombre, categoria, descripcion, precio) VALUES
('Hemograma Completo', 'Hematología', 'Análisis completo de células sanguíneas', 80.00),
('Glucosa en Ayunas', 'Bioquímica', 'Medición de niveles de glucosa en sangre', 30.00),
('Perfil Lipídico', 'Bioquímica', 'Colesterol total, HDL, LDL y triglicéridos', 120.00),
('Examen General de Orina', 'Uroanálisis', 'Análisis físico, químico y microscópico de orina', 25.00),
('Creatinina', 'Bioquímica', 'Evaluación de función renal', 35.00),
('Transaminasas (TGO/TGP)', 'Bioquímica', 'Evaluación de función hepática', 60.00),
('TSH', 'Hormonas', 'Hormona estimulante de tiroides', 90.00),
('Proteína C Reactiva', 'Inmunología', 'Marcador de inflamación', 70.00);

-- Verificar datos insertados
SELECT COUNT(*) as total_pruebas FROM pruebas;

-- ============================================================
-- RESULTADO ESPERADO
-- ============================================================
-- ✅ 4 tablas creadas: usuarios, pacientes, resultados, pruebas
-- ✅ Todas las tablas vacías (excepto pruebas si insertaste los ejemplos)
-- ✅ Índices creados para mejorar rendimiento
-- ✅ Foreign keys configuradas correctamente
-- ============================================================

-- ============================================================
-- SIGUIENTE PASO:
-- ============================================================
-- Ejecuta en tu computadora:
-- python create_admin.py
--
-- Esto creará el usuario administrador:
-- Usuario: DoctorMauricoPerezPTS574
-- Contraseña: Cachuchin574 (hasheada)
-- ============================================================

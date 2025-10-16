-- Elimina las tablas viejas si existen, para empezar de cero
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS products;

-- Crear la tabla para Equipos (Equipment)
CREATE TABLE equipment (
    id UUID PRIMARY KEY,
    data JSONB
);

-- Crear la tabla para Productos (Products)
CREATE TABLE products (
    id UUID PRIMARY KEY,
    data JSONB
);
BEGIN;

-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    full_name VARCHAR(255),
    phone_number VARCHAR(15),
    gender VARCHAR(10),
    birth_date DATE,
    provider VARCHAR(50),
    provider_user_id VARCHAR(255),
    provider_data JSONB
);

-- Индекс для быстрого поиска по email
CREATE INDEX idx_users_email ON users (email);

-- Индекс для быстрого поиска по OAuth ID
CREATE INDEX idx_users_provider_user_id ON users (provider_user_id);

-- Таблица ролей
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Таблица прав
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Связь между ролями и правами
CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- Связь между пользователями и ролями
CREATE TABLE user_roles (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Добавляем примеры данных
INSERT INTO roles (name, description) VALUES
('admin', 'Administrator role'),
('user', 'Regular user role');

INSERT INTO permissions (name, description) VALUES
('view_logs', 'View system logs'),
('edit_users', 'Edit user accounts');

COMMIT;

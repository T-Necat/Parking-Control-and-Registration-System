-- Rolls back the database to its initial state
INSERT INTO roles (role_name, description) VALUES
('admin', 'System administrator'),
('manager', 'Parking manager'),
('user', 'Standard user');

-- Users table
INSERT INTO users (username, password, role_id) VALUES
('admin', 'admin123', 1),
('manager', 'manager123', 2);


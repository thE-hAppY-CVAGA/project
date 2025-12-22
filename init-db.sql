-- Экспорт данных из базы shoe_sales-db
-- Автоматически сгенерировано скриптом export_db.py

-- Данные таблицы customers (1 записей)
INSERT INTO customers (id, name, phone, email, address, created_at, inn) VALUES (1, 'ООО "Обувь всем"', '+8(999)99-99-99', 'skdvs@', 'Киров, Солнечная 15', 2025-12-21 16:06:14.261339, '1234567890123456');

-- Данные таблицы products (2 записей)
INSERT INTO products (id, name, size, price, quantity, created_at, cost_price) VALUES (1, 'Кроссовки Nike Air Max 45', '45', 3500.00, 40, 2025-12-21 15:37:33.834800, 0.00);
INSERT INTO products (id, name, size, price, quantity, created_at, cost_price) VALUES (2, 'Кроссовки Nilke Air Force 1', '42', 10000.00, 100, 2025-12-21 16:05:27.205294, 0.00);

-- Данные таблицы sale_items (1 записей)
INSERT INTO sale_items (id, sale_id, product_id, quantity, price) VALUES (2, 1, 1, 10, 3500.00);

-- Данные таблицы sales (1 записей)
INSERT INTO sales (id, customer_id, user_id, total_amount, sale_date, status) VALUES (1, 1, 1, 35000.00, 2025-12-21 16:09:54.072403, 'completed');

-- Данные таблицы users (2 записей)
INSERT INTO users (id, username, password_hash, role, created_at) VALUES (1, 'admin', '$2b$12$u8TfGwS76j7.jrWy9jSWfegLwfTlyvf9ebKyVd8LAmP22TuKoxf2i', 'admin', 2025-12-20 22:00:45.759294);
INSERT INTO users (id, username, password_hash, role, created_at) VALUES (2, 'user', '$2b$12$bt2KWuXu.4FhUOjJV7DOieHIaWWKNjL/GAez7XJWBBsiH1p0Z4B.e', 'user', 2025-12-21 15:07:18.872330);

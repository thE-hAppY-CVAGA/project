import psycopg2
import configparser
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import bcrypt

def load_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    if not config.has_section('postgres'):
        raise ValueError("Секция [postgres] отсутствует в config.ini")

    required_params = ['host', 'port', 'database', 'user', 'password']
    params = {}

    for param in required_params:
        if not config.has_option('postgres', param):
            raise KeyError(f"Отсутствуют параметры в конфиге [postgres]: {[param]}")
        params[param] = config.get('postgres', param).strip()

    return params

class DB:
    def __init__(self):
        self.params = load_db_config()
        self.connection = None
        self.connect()

    def connect(self):

        try:
            clean_params = {}
            for key, value in self.params.items():
                clean_value = ''.join(c for c in str(value) if ord(c) < 128).strip()
                clean_params[key] = clean_value

            dsn = (
                f"host={clean_params['host']} "
                f"port={clean_params['port']} "
                f"dbname={clean_params['database']} "
                f"user={clean_params['user']} "
                f"password={clean_params['password']} "
                f"client_encoding=UTF8"
            )
            self.connection = psycopg2.connect(dsn)
            self.connection.autocommit = True

            # Создаем таблицы при подключении
            self.create_tables()
        except KeyboardInterrupt:
            print("\nПодключение к базе данных прервано пользователем")
            raise
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def execute_query(self, query, params=None, fetch=False):
        """Выполняет SQL запрос"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                return True
        except KeyboardInterrupt:
            print("\nВыполнение SQL запроса прервано пользователем")
            raise
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.connection.rollback()
            raise

    def create_tables(self):

        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                size VARCHAR(10),
                price DECIMAL(10,2) NOT NULL,
                quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            -- Добавляем поле inn, если его нет
            ALTER TABLE customers ADD COLUMN IF NOT EXISTS inn VARCHAR(16)
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                user_id INTEGER REFERENCES users(id),
                total_amount DECIMAL(10,2) NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'completed'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER REFERENCES sales(id),
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
            """
        ]

        for i, query in enumerate(queries):
            if not query or not query.strip():
                print(f"Пропускаю пустой запрос #{i}")
                continue
            print(f"Выполняю запрос #{i}: {query[:50]}...")
            self.execute_query(query)

        self.create_default_admin()

    def create_default_admin(self):

        try:

            result = self.execute_query(
                "SELECT id FROM users WHERE username = 'admin'",
                fetch=True
            )

            if not result:

                password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.execute_query(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    ('admin', password_hash, 'admin')
                )
                print("Создан пользователь admin с паролем 'admin123'")
        except Exception as e:
            print(f"Ошибка создания администратора: {e}")

    def authenticate_user(self, username, password):

        try:
            result = self.execute_query(
                "SELECT id, username, password_hash, role FROM users WHERE username = %s",
                (username,),
                fetch=True
            )

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]['password_hash'].encode('utf-8')):
                return {
                    'id': result[0]['id'],
                    'username': result[0]['username'],
                    'role': result[0]['role']
                }
            return None
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return None

    def get_products(self):

        return self.execute_query(
            "SELECT * FROM products ORDER BY name",
            fetch=True
        )

    def get_customers(self):

        return self.execute_query(
            "SELECT * FROM customers ORDER BY name",
            fetch=True
        )

    def get_sales(self, limit=100):
 
        return self.execute_query(
            """
            SELECT s.*, c.name as customer_name, u.username,
                   COUNT(DISTINCT si.product_id) as items_count
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            LEFT JOIN users u ON s.user_id = u.id
            LEFT JOIN sale_items si ON s.id = si.sale_id
            GROUP BY s.id, c.name, u.username
            ORDER BY s.sale_date DESC
            LIMIT %s
            """,
            (limit,),
            fetch=True
        )

    def close(self):

        if self.connection:
            self.connection.close()

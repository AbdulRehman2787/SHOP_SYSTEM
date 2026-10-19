"""
Database Connection and Initialization Module
Uses mysql-connector-python with UTF-8 encoding and transaction support.
"""

import os
from contextlib import contextmanager
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

# Load environment variables from .env file
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2787")
DB_NAME = os.getenv("DB_NAME", "shop_management_db")


def get_server_connection():
    """Connect to MySQL Server directly (without selecting a database)"""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=False
    )


def get_db_connection():
    """Connect to the specific application database with utf8mb4 encoding"""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=False
    )


@contextmanager
def get_db():
    """
    Context manager for database transactions.
    Automatically commits on normal exit and rolls back on any exception.
    """
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """
    Ensure the database, tables, and default products exist.
    Called automatically on application startup.
    """
    # 1. Create database if it does not exist
    server_conn = get_server_connection()
    server_cur = server_conn.cursor()
    server_cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
        f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    server_cur.close()
    server_conn.close()

    # 2. Connect to database and create tables
    with get_db() as conn:
        cursor = conn.cursor()

        # Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name_en VARCHAR(100) NOT NULL UNIQUE,
                name_ur VARCHAR(100) NOT NULL,
                category VARCHAR(50) DEFAULT 'Home Appliance',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Purchases Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                purchase_date DATE NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(12, 2) NOT NULL,
                transport_cost DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
                total_cost DECIMAL(12, 2) NOT NULL,
                effective_unit_cost DECIMAL(12, 2) NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_purchase_product FOREIGN KEY (product_id) 
                    REFERENCES products(id) ON DELETE RESTRICT,
                CONSTRAINT chk_purchase_qty CHECK (quantity > 0),
                CONSTRAINT chk_purchase_price CHECK (unit_price >= 0),
                CONSTRAINT chk_purchase_transport CHECK (transport_cost >= 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Sales Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                sale_date DATE NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(12, 2) NOT NULL,
                total_amount DECIMAL(12, 2) NOT NULL,
                unit_cost_at_sale DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_sale_product FOREIGN KEY (product_id) 
                    REFERENCES products(id) ON DELETE RESTRICT,
                CONSTRAINT chk_sale_qty CHECK (quantity > 0),
                CONSTRAINT chk_sale_price CHECK (unit_price >= 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Expenses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(12, 2) NOT NULL,
                expense_date DATE NOT NULL,
                for_month VARCHAR(7) NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT chk_expense_amount CHECK (amount > 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 3. Seed Default 4 Home Appliances
        default_products = [
            (1, "Refrigerator", "ریفریجریٹر", "Home Appliance"),
            (2, "Air Cooler", "ایئر کولر", "Home Appliance"),
            (3, "Air Conditioner (AC)", "ایئر کنڈیشنر (اے سی)", "Home Appliance"),
            (4, "Washing Machine", "واشنگ مشین", "Home Appliance")
        ]

        for pid, name_en, name_ur, cat in default_products:
            cursor.execute("""
                INSERT INTO products (id, name_en, name_ur, category)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    name_en = VALUES(name_en),
                    name_ur = VALUES(name_ur);
            """, (pid, name_en, name_ur, cat))

        cursor.close()

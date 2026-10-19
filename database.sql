-- ========================================================
-- Shop Stock and Accounts Management System
-- Database Schema for MySQL 8.0+
-- Encoding: UTF-8 (utf8mb4) for complete Urdu support
-- ========================================================

CREATE DATABASE IF NOT EXISTS shop_management_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE shop_management_db;

-- 1. Products Table (چار بنیادی اشیاء)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL UNIQUE,
    name_ur VARCHAR(100) NOT NULL,
    category VARCHAR(50) DEFAULT 'Home Appliance',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Purchases Table (نیا مال آیا / خریداری)
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

-- 3. Sales Table (مال فروخت ہوا / سیلز)
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

-- 4. Expenses Table (دکان کے اخراجات)
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- 'rent', 'salary', 'electricity', 'other'
    amount DECIMAL(12, 2) NOT NULL,
    expense_date DATE NOT NULL,
    for_month VARCHAR(7) NULL,      -- e.g. '2026-10' for tracking monthly rent/salary
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_expense_amount CHECK (amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Seed Initial 4 Home Appliances
INSERT INTO products (id, name_en, name_ur, category)
VALUES 
    (1, 'Refrigerator', 'ریفریجریٹر', 'Home Appliance'),
    (2, 'Air Cooler', 'ایئر کولر', 'Home Appliance'),
    (3, 'Air Conditioner (AC)', 'ایئر کنڈیشنر (اے سی)', 'Home Appliance'),
    (4, 'Washing Machine', 'واشنگ مشین', 'Home Appliance')
ON DUPLICATE KEY UPDATE 
    name_en = VALUES(name_en), 
    name_ur = VALUES(name_ur);

-- ==========================================
-- BANK MANAGEMENT SYSTEM DATABASE
-- ==========================================

CREATE DATABASE IF NOT EXISTS bank_management_system;

-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS bank_management_system.users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)     NOT NULL UNIQUE,
    password_hash VARCHAR(64)     NOT NULL,
    balance       DECIMAL(12, 2)  NOT NULL DEFAULT 0,
    created_at    TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TRANSACTIONS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS bank_management_system.transactions (
    transaction_id   INT AUTO_INCREMENT PRIMARY KEY,
    sender_id        INT,
    receiver_id      INT,
    transaction_type ENUM('DEPOSIT', 'WITHDRAW', 'TRANSFER_IN', 'TRANSFER_OUT') NOT NULL,
    amount           DECIMAL(12, 2) NOT NULL,
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id)   REFERENCES bank_management_system.users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES bank_management_system.users(id) ON DELETE CASCADE
);

-- ==========================================
-- ADMINS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS bank_management_system.admins (
    admin_id      INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64)        NOT NULL
);

-- ==========================================
-- DEFAULT ADMIN
-- Username : shubham
-- Password : admin123
-- ==========================================

INSERT IGNORE INTO bank_management_system.admins (admin_id, username, password_hash)
VALUES (1, 'shubham', '10f6d3ce9d854d1ebfc1ca7d1981fafc122a9970093382f2c5c72cfa6ab47572');
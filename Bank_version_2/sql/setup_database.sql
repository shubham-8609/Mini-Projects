-- ==========================================
-- BANK MANAGEMENT SYSTEM DATABASE
-- ==========================================

DROP DATABASE IF EXISTS bank_management_system;

CREATE DATABASE bank_management_system;

USE bank_management_system;

-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password_hash VARCHAR(64) NOT NULL,

    balance DECIMAL(12,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================================
-- TRANSACTIONS TABLE
-- ==========================================

CREATE TABLE transactions (

    transaction_id INT AUTO_INCREMENT PRIMARY KEY,

    sender_id INT,

    receiver_id INT,

    transaction_type ENUM(
    'DEPOSIT',
    'WITHDRAW',
    'TRANSFER_IN',
    'TRANSFER_OUT'
),

    amount DECIMAL(12,2) NOT NULL,

    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(sender_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY(receiver_id)
        REFERENCES users(id)
        ON DELETE CASCADE

);

-- ==========================================
-- ADMINS TABLE
-- ==========================================

CREATE TABLE admins (

    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL,

    password_hash VARCHAR(64) NOT NULL

);

-- ==========================================
-- DEFAULT ADMIN
-- Username : admin
-- Password : admin123
-- (We'll replace this hash later from Python.)
-- ==========================================

INSERT INTO admins(username,password_hash)

insert into admins values(1 , "shubham" , "10f6d3ce9d854d1ebfc1ca7d1981fafc122a9970093382f2c5c72cfa6ab47572");
-- PostgreSQL Setup Script for Zyndle AI
-- Run this script as the postgres superuser

-- Create a new user for the application
CREATE USER zyndle_user WITH PASSWORD 'zyndle_password_2024';

-- Create the database
CREATE DATABASE zyndle_ai OWNER zyndle_user;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE zyndle_ai TO zyndle_user;

-- Connect to the zyndle_ai database
\c zyndle_ai;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO zyndle_user;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify the setup
SELECT current_database(), current_user; 
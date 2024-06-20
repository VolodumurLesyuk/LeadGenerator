-- Створення користувача, якщо його ще не існує
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'admin') THEN
    CREATE USER admin WITH SUPERUSER PASSWORD 'admin';
  END IF;
END $$;

-- Створення бази даних, якщо вона ще не існує
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'konch1') THEN
    CREATE DATABASE testova OWNER admin;
  END IF;
END $$;
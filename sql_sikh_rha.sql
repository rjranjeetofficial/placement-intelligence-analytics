-- =========================================================
-- SQL PRACTICE DATABASE
-- Author: Ranjeet Kumar - AIML Engineer
-- =========================================================

CREATE DATABASE sql_practice;

USE sql_practice;


-- =========================================================
-- 1. DEPARTMENT TABLE
-- =========================================================

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    location VARCHAR(50)
);


INSERT INTO departments
(department_id, department_name, location)
VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Mumbai'),
(4, 'Marketing', 'Bangalore'),
(5, 'Sales', 'Pune');


-- =========================================================
-- 2. EMPLOYEE TABLE
-- =========================================================

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50),
    age INT,
    gender VARCHAR(10),
    salary DECIMAL(10,2),
    city VARCHAR(50),
    department_id INT,
    joining_date DATE,
    email VARCHAR(100),
    manager_id INT,
    
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);


INSERT INTO employees
(employee_id, employee_name, age, gender, salary, city,
 department_id, joining_date, email, manager_id)
VALUES
(101, 'Ranjeet', 22, 'Male', 55000, 'Delhi',
 1, '2024-01-15', 'ranjeet@gmail.com', NULL),

(102, 'Aman', 25, 'Male', 65000, 'Noida',
 1, '2023-06-10', 'aman@gmail.com', 101),

(103, 'Priya', 24, 'Female', 60000, 'Delhi',
 2, '2023-08-20', 'priya@gmail.com', 101),

(104, 'Rahul', 28, 'Male', 80000, 'Mumbai',
 3, '2022-04-12', 'rahul@gmail.com', NULL),

(105, 'Neha', 26, 'Female', 72000, 'Bangalore',
 4, '2022-11-05', 'neha@gmail.com', 104),

(106, 'Vikas', 30, 'Male', 90000, 'Pune',
 5, '2021-03-18', 'vikas@gmail.com', NULL),

(107, 'Anjali', 23, 'Female', 50000, 'Noida',
 2, '2024-02-01', 'anjali@gmail.com', 103),

(108, 'Karan', 27, 'Male', 75000, 'Delhi',
 1, '2022-07-25', 'karan@gmail.com', 101),

(109, 'Sneha', 29, 'Female', 85000, 'Mumbai',
 3, '2021-09-15', 'sneha@gmail.com', 104),

(110, 'Arjun', 24, 'Male', 58000, 'Pune',
 5, '2024-03-10', 'arjun@gmail.com', 106);


-- =========================================================
-- 3. PROJECTS TABLE
-- =========================================================

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100),
    budget DECIMAL(12,2),
    start_date DATE,
    department_id INT,
    
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);


INSERT INTO projects
(project_id, project_name, budget, start_date, department_id)
VALUES
(201, 'AI Chatbot', 500000, '2024-01-01', 1),
(202, 'Employee Portal', 300000, '2023-05-15', 1),
(203, 'Recruitment System', 250000, '2023-07-10', 2),
(204, 'Financial Dashboard', 700000, '2022-03-20', 3),
(205, 'Marketing Analytics', 450000, '2022-10-01', 4),
(206, 'Sales Prediction', 600000, '2021-12-15', 5);


-- =========================================================
-- 4. EMPLOYEE_PROJECT TABLE
-- =========================================================

CREATE TABLE employee_project (
    employee_id INT,
    project_id INT,
    hours_worked INT,
    
    PRIMARY KEY (employee_id, project_id),
    
    FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id),
    
    FOREIGN KEY (project_id)
    REFERENCES projects(project_id)
);


INSERT INTO employee_project
(employee_id, project_id, hours_worked)
VALUES
(101, 201, 120),
(102, 201, 150),
(102, 202, 100),
(103, 203, 130),
(104, 204, 160),
(105, 205, 140),
(106, 206, 170),
(108, 202, 110),
(109, 204, 145),
(110, 206, 125);


-- =========================================================
-- CHECK OUR DATABASE
-- =========================================================

SHOW TABLES;

SELECT * FROM departments;

SELECT * FROM employees;

SELECT * FROM projects;

SELECT * FROM employee_project;
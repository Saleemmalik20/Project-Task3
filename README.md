-- Creating a Database named student_management
CREATE DATABASE student_management;

-- Using Database student_management
USE student_management; 

-- Creating student table
CREATE TABLE students (
	id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    course VARCHAR(50) NOT NULL,
    enrolled_on DATE NOT NULL DEFAULT (CURRENT_DATE)
); 

SELECT * FROM students;

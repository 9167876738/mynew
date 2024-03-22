CREATE DATABASE hostel_db;

USE hostel_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    check_in_date DATE,
    check_out_date DATE,
    room_type VARCHAR(50),
    FOREIGN KEY (room_type) REFERENCES room_types(type)
);

CREATE TABLE room_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50)
);

-- Inserting default room types
INSERT INTO room_types (type) VALUES ('Single'), ('Double'), ('Triple');

-- Viewing tables
SELECT * FROM bookings;

SELECT * FROM students;

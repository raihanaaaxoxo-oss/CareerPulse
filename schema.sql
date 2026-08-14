CREATE DATABASE careerpulse_db;

USE careerpulse_db;

CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications(
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company VARCHAR(150) NOT NULL,
    role_title VARCHAR(150) NOT NULL,
    status ENUM(
		'Applied',
        'Screening',
        'Interviewing',
        'Offer',
        'Rejected'
	) DEFAULT 'Applied',
	applied_date DATE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    

	FOREIGN KEY (user_id)
		REFERENCES users(id)
		ON DELETE CASCADE
);
CREATE DATABASE IF NOT EXISTS workforce_dashboard;

USE workforce_dashboard;

DROP TABLE IF EXISTS workforce_productivity;

CREATE TABLE workforce_productivity (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10) NOT NULL,
    team_id VARCHAR(20),
    department VARCHAR(30),
    role_function VARCHAR(40),
    manager_id VARCHAR(10),
    location_site VARCHAR(20),
    period_date DATE NOT NULL,
    hours_planned DECIMAL(6,1),
    hours_worked DECIMAL(6,1),
    overtime_hours DECIMAL(6,1),
    absence_days DECIMAL(5,1),
    output_units INT,
    unit_value DECIMAL(10,2),
    quality_score DECIMAL(5,1),
    error_count INT,
    attrition_flag BOOLEAN,
    date_joined DATE,
    date_left DATE,
    engagement_score DECIMAL(4,2),
    total_labor_cost DECIMAL(12,2),
    headcount INT DEFAULT 1,

    INDEX idx_employee (employee_id),
    INDEX idx_team (team_id),
    INDEX idx_department (department),
    INDEX idx_period (period_date),
    INDEX idx_manager (manager_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
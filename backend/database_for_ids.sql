-- 1. Pehle database create karo
CREATE DATABASE arp_ids;

-- 2. Us database ko select karo
USE arp_ids;

-- 3. Ab alerts save karne ke liye table banao
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attacker_mac VARCHAR(17) NOT NULL,
    target_ip VARCHAR(15) NOT NULL,
    alert_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM alerts;
-- Basic Analytics

-- Average waiting time per department
SELECT department, AVG(waiting_time) AS avg_waiting_time
FROM visits
GROUP BY department;

-- Daily patient count
SELECT CAST(admission_time AS DATE) AS date, COUNT(*) AS daily_patients
FROM visits
GROUP BY CAST(admission_time AS DATE);

-- No-show percentage
SELECT department,
       COUNT(*) AS total_appointments,
       SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS no_show_rate
FROM appointments
GROUP BY department;

-- Intermediate

-- Peak hour patient inflow
SELECT EXTRACT(HOUR FROM admission_time) AS hour_of_day, COUNT(visit_id) AS patient_count
FROM visits
GROUP BY EXTRACT(HOUR FROM admission_time)
ORDER BY patient_count DESC;

-- Doctor workload distribution
SELECT doctor_id, COUNT(visit_id) AS total_visits
FROM visits
GROUP BY doctor_id
ORDER BY total_visits DESC;

-- Department-wise congestion ranking
SELECT department, AVG(waiting_time) AS avg_waiting
FROM visits
GROUP BY department
ORDER BY avg_waiting DESC;

-- Advanced (Important)

-- Top 10 patients with repeated no-shows
SELECT patient_id, COUNT(*) AS no_show_count
FROM appointments
WHERE status = 'No-show'
GROUP BY patient_id
ORDER BY no_show_count DESC
LIMIT 10;

-- Waiting time percentile using window functions
SELECT patient_id, department, waiting_time,
       NTILE(100) OVER (PARTITION BY department ORDER BY waiting_time) AS waiting_time_percentile
FROM visits;

-- Running total of daily patients
SELECT appointment_date, 
       COUNT(appointment_id) AS daily_patients,
       SUM(COUNT(appointment_id)) OVER (ORDER BY appointment_date) AS running_total
FROM appointments
GROUP BY appointment_date;

-- Departments with highest no-show impact
SELECT department,
       COUNT(*) AS total_appointments,
       SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows
FROM appointments
GROUP BY department
ORDER BY no_shows DESC;

-- 01_doctors_schedule.sql
INSERT INTO doctors_schedule (
        doctor_name,
        specialty,
        available_days,
        start_time,
        end_time
    )
VALUES (
        'Dr. Andi Wirawan',
        'Cardiology',
        'Senin–Jumat',
        '08:00:00',
        '12:00:00'
    ),
    (
        'Dr. Andi Wirawan',
        'Cardiology',
        'Senin–Jumat',
        '13:00:00',
        '16:00:00'
    ),
    (
        'Dr. Budi Santoso',
        'Dermatology',
        'Selasa, Kamis',
        '09:00:00',
        '12:00:00'
    ),
    (
        'Dr. Citra Mahendra',
        'Pediatrics',
        'Senin–Sabtu',
        '10:00:00',
        '14:00:00'
    ),
    (
        'Dr. Dian Pratiwi',
        'Neurology',
        'Rabu, Jumat',
        '14:00:00',
        '18:00:00'
    );
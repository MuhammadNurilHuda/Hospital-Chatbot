-- 02_hospital_faq.sql
INSERT INTO hospital_faq (question, answer)
VALUES (
        'Bagaimana cara membuat janji temu?',
        'Ketik ''booking'' pada chat, pilih dokter dan tanggal, lalu konfirmasi.'
    ),
    (
        'Dokumen apa yang diperlukan saat datang?',
        'Siapkan KTP, kartu asuransi/BPJS, dan rekam medis (jika ada).'
    ),
    (
        'Berapa biaya konsultasi dokter umum?',
        'Biaya mulai dari Rp150.000 untuk pasien umum; diskon 20% untuk pasien BPJS.'
    ),
    (
        'Bagaimana cara membatalkan janji temu?',
        'Ketik ''batal'' pada chat minimal 24 jam sebelum jadwal atau hubungi call center.'
    ),
    (
        'Jam besuk pasien di rumah sakit?',
        'Setiap hari pukul 09:00–17:00, maksimal 2 orang per pasien.'
    );
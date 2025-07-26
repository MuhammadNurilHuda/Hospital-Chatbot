-- 04_appointment_process.sql
INSERT INTO appointment_process (step_order, title, description) VALUES
  (1, 'Mulai Chat', 'User memulai dengan mengirim kata kunci “booking” ke chatbot.'),
  (2, 'Pilih Dokter', 'Chatbot menampilkan daftar spesialisasi dan nama dokter, user memilih salah satu.'),
  (3, 'Pilih Tanggal & Waktu', 'Chatbot menanyakan tanggal dan slot waktu yang tersedia untuk dokter tersebut.'),
  (4, 'Isi Data Pasien', 'User memasukkan nama lengkap, nomor telepon, dan nomor asuransi (jika ada).'),
  (5, 'Konfirmasi & Simpan', 'Chatbot memberikan ringkasan booking dan `appointment_id`, lalu menyimpan data ke database.'),
  (6, 'Notifikasi', 'Sistem mengirim SMS atau email pemberitahuan 1 hari sebelum jadwal.');

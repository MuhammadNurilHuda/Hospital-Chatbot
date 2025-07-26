-- 05_emergency_services.sql
INSERT INTO emergency_services (service_name, description, contact) VALUES
  ('Unit Gawat Darurat (UGD)',
   'Operasional 24/7 untuk kasus darurat medis',
   '(021) 555-9999'),
  ('Ambulans',
   'Layanan ambulans cepat, pesan via chatbot dengan format: “ambulans + lokasi”',
   'chatbot command'),
  ('Hotline COVID-19',
   'Info dan konsultasi COVID-19 tanpa biaya',
   '1500-567'),
  ('Kebijakan Kunjungan',
   'Maksimal 2 orang per pasien, wajib gunakan APD (masker, face shield)',
   '—');

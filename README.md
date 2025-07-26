# AI Agents for Hospital Appointment Booking

# Hospital Chatbot Project

Proyek **Hospital Chatbot** bertujuan untuk membangun aplikasi berbasis AI/Chatbot yang membantu pasien memesan janji temu dokter dan memberikan respon percakapan yang lebih interaktif. Aplikasi ini dibangun menggunakan **FastAPI**, **PostgreSQL** (melalui SQLAlchemy), dan mengintegrasikan **DeepSeek API** untuk pemrosesan bahasa alami.

## 1. Deskripsi Proyek

1. **Fokus Utama**

   - Membantu pasien dalam _booking appointment_ dengan dokter.
   - Menyediakan sistem _logging & monitoring_ untuk setiap percakapan.
   - Menyimpan riwayat percakapan (prompt & response) di database sebagai _user activity logs_.
   - Mendukung kelanjutan pengembangan seperti _session management_ (Redis) dan _human escalation_ (CS).

2. **Kegunaan Chatbot**

   - Menjawab pertanyaan seputar informasi dokter & jadwal.
   - Memfasilitasi proses pemesanan janji temu (appointment) secara otomatis.
   - Mencatat detail percakapan untuk keperluan audit, analisis, atau keluhan pasien.

3. **Teknologi Utama**
   - **FastAPI** + Python untuk server API.
   - **DeepSeek API** (NLP) untuk pemahaman percakapan.
   - **PostgreSQL** dan **SQLAlchemy ORM** untuk database.
   - **dotenv (.env)** untuk konfigurasi rahasia (API Key, URL DB).
   - Rencana **Docker + Kubernetes** untuk produksi.

---

## 2. Struktur Direktori

Berikut struktur utama direktori proyek:

    AI-Agents-Hospital-Booking/
    ├── app/
    │   ├── main.py               # Entry point FastAPI
    │   ├── chatbot.py            # Modul AI Chatbot (DeepSeek API)
    │   ├── database.py           # Konfigurasi PostgreSQL & Model DB
    │   ├── models.py             # (Opsional, jika dipisah)
    │   ├── logging.py            # Menggunakan logging.conf eksternal
    │   ├── session.py            # (Planned) Manajemen session (Redis)
    │   ├── error_handler.py      # (Opsional) Modul penanganan error/exception
    ├── tests/
    │   ├── test_main.py          # Test endpoint (root, /chat, /appointment/book)
    │   ├── test_chatbot.py       # Test chatbot (logika & mock DeepSeek API)
    │   ├── test_database.py      # Test DB (appointments, user_activity_logs)
    ├── migrations/               # (Planned) Folder migrasi DB (Alembic)
    ├── config/                   # (Planned) Konfigurasi (settings, constants)
    │   ├── settings.py
    │   ├── constants.py
    ├── scripts/
    │   └── init_db.py            # Skrip inisialisasi database
    ├── logs/                     # Folder file log
    ├── configs/
    │   └── logging.conf          # File konfigurasi logging eksternal
    ├── requirements.txt          # Daftar library Python
    ├── .env                      # Konfigurasi rahasia (API Key, DB URL)
    ├── .gitignore                # Daftar file/folder diabaikan oleh Git
    ├── Dockerfile                # (Planned) Konfigurasi Docker image
    ├── docker-compose.yml        # (Planned) Orkestrasi Docker container
    └── README.md                 # Dokumentasi proyek

---

## 3. Fitur yang Selesai

1. **FastAPI + DeepSeek API**

   - Endpoint `/chat` memanggil fungsi `get_response` (di `chatbot.py`) untuk memproses percakapan.
   - Chatbot mendeteksi intent booking melalui kata kunci sederhana, lalu menampilkan instruksi booking.

2. **Database PostgreSQL**

   - Menggunakan **SQLAlchemy** untuk operasi DB.
   - Tabel `appointments` (menyimpan data booking dokter) dan `user_activity_logs` (menyimpan riwayat percakapan).

3. **Endpoint `/appointment/book`**

   - Menerima data booking (nama, telepon, spesialisasi, tanggal).
   - Menyimpan data ke tabel `appointments`.

4. **Logging Dasar**

   - Memakai `logging.conf` (eksternal) di `configs/logging.conf`.
   - Memanggil `logging.config.fileConfig(CONFIG_PATH)` di `app/logging.py`.
   - Log ditulis ke console dan file (misal: `logs/chatbot.log`).

5. **Pengujian (Pytest)**
   - `test_main.py`: Test endpoint `/`, `/chat`, `/appointment/book`.
   - `test_chatbot.py`: Test fungsi `get_response`, penggunaan `monkeypatch` untuk mock API eksternal.
   - `test_database.py`: Test koneksi DB, penyimpanan data di `appointments` & `user_activity_logs`.
   - Fixture `Base.metadata.create_all` memastikan tabel dibuat sebelum test, `drop_all` setelahnya.

---

## 4. Sprint Progress

**Sprint 1 - Setup Dasar**

- Membuat repo, mengatur environment.
- Endpoint `/chat` + integrasi awal DeepSeek.
- **Status:** Selesai

**Sprint 2 - Chatbot Intent Booking**

- Mendeteksi intent booking vs permintaan info dokter.
- Chatbot meminta detail booking (nama, jadwal, dsb.).
- **Status:** Selesai

**Sprint 3 - DB & Booking**

- Setup PostgreSQL & tabel `appointments`.
- Endpoint `/appointment/book` untuk simpan data.
- **Status:** Selesai

**Sprint 4 - Logging & Fallback**

- Log percakapan di `user_activity_logs`.
- Rencana fallback ke CS jika chatbot gagal merespons.
- **Status:** In Progress

---

## 5. Rencana Pengembangan

1. **Session Management**

   - Gunakan Redis untuk menyimpan konteks percakapan lintas request.

2. **Logging & Monitoring Terpusat**

   - Integrasi dengan ELK Stack atau Prometheus + Grafana.

3. **Deployment**

   - Dockerfile, docker-compose untuk memudahkan deployment.

4. **Auth & User Management**

   - Tabel `users`, relasi dengan `user_activity_logs` untuk multi-user real.

5. **Fallback ke CS**

   - Alur eskalasi jika chatbot tidak mengenali intent.

6. **NLP Lanjutan**
   - Menggantikan keyword matching dengan model custom, spaCy, atau transformers.

---

## 6. Cara Menjalankan

1.  **Instal Dependencies**

    ```
    pip install -r requirements.txt
    ```

2.  **Konfigurasi Environment**

    - Buat file `.env` isi minimal:

          DEEPSEEK_API_KEY=<key>
          DATABASE_URL=postgresql://username:password@localhost:5432/hospital_db

3.  **Inisialisasi Database**

    - Pastikan PostgreSQL aktif.
    - Gunakan `Base.metadata.create_all(bind=engine)` atau jalankan skrip SQL untuk membuat tabel.

4.  **Menjalankan Server**

    ```
    uvicorn app.main:app --reload
    ```

    - Akses di `http://127.0.0.1:8000`.

5.  **Testing**
    ```
    pytest tests/
    ```
    - Jalankan semua test (unit & integration).

---

## 7. Pengujian dengan Postman

1.  **Root Endpoint** (`GET /`)
    - Response OK `{"message": "Hospital Chatbot API is running!"}`
2.  **Chat Endpoint** (`POST /chat`)
    - Body JSON misal: `{"message": "Bagaimana cuaca hari ini?"}`
    - Periksa response & status code `200`.
3.  **Booking Endpoint** (`POST /appointment/book`)

    - Body JSON:

          {
            "name": "John Doe",
            "phone": "08123456789",
            "doctor_specialist": "Cardiology",
            "appointment_date": "2025-03-10"
          }

    - Status code `200`, response mengandung `"appointment_id"`.

---

## 8. Kontak

- **Nama**: Muhammad Nuril Huda
- **Email**: muhammadnurilhuda@mail.ugm.ac.id

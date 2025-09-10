README – Chatbot Customer Support


**1. Persiapan Environment**

Sebelum memulai, pastikan Anda sudah menginstal:

Python ≥ 3.9

pip (Python package manager)

virtualenv (opsional, untuk isolasi environment)

SQLite (sudah tersedia default di Python)

Docker (untuk kontainerisasi, opsional tapi direkomendasikan)

**2. Clone & Struktur Project**

Clone repository ini, lalu masuk ke folder project. Struktur folder utamanya:

project-root/
│── app/
│   ├── db.py
│   ├── llm.py
│   ├── main.py
│   ├── prompts.py
│   ├── tools.py
│── schema.sql
│── requirements.txt
│── Dockerfile

**3.Instalasi Dependencies**

Buat virtual environment (opsional tapi disarankan):
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Lalu install dependencies:

pip install -r requirements.txt

**4. Setup Database**

Inisialisasi database SQLite (chatbot.db) sesuai schema, buka lokasi project menggunakan cd:

sqlite3 chatbot.db < schema.sql

**5. Menjalankan Aplikasi**

Jalankan API server dengan Uvicorn:

uvicorn app.main:app --reload

**6. API Endpoints**

Beberapa endpoint utama:

GET /health → cek status server

POST /conversations → buat percakapan baru

POST /chat → kirim pesan ke chatbot

GET /conversations/{cid}/messages → lihat riwayat chat


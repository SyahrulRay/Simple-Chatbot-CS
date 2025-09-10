README

# 🤖 Chatbot Customer Support

<p align="center">
  <img src="assets/logo.png" alt="Chatbot Logo" width="200"/>
</p>

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📖 About
Chatbot Customer Support adalah aplikasi berbasis FastAPI yang terintegrasi dengan LLM (Ollama) 
untuk membantu pelanggan mengecek status pesanan, informasi produk, dan kebijakan garansi.


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



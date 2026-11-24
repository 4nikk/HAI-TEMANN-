# Website Anik — Flask

## Isi project
- `app.py` — seluruh halaman, animasi, validasi formulir, dan pengiriman email.
- `static/tahu-tek.jpg` — ilustrasi tahu tek yang kamu unggah.
- `requirements.txt` — dependensi Python.
- `Procfile` — perintah untuk menjalankan aplikasi di Render.

## Menjalankan di komputer
1. Install Python 3.10 atau lebih baru.
2. Buka terminal di folder project.
3. Jalankan `pip install -r requirements.txt`.
4. Atur variabel email (lihat bagian konfigurasi email).
5. Jalankan `python app.py`, lalu buka `http://127.0.0.1:5000`.

## Konfigurasi email Gmail
Aplikasi mengirim:
- Jawaban kuis atau pesan dan kesan ke `anikdansafitri@gmail.com`.
- Email ucapan terima kasih ke alamat email yang diisi pengunjung.

Untuk keamanan, jangan tulis password Gmail di `app.py` dan jangan unggah password ke GitHub.
Gunakan Gmail App Password (bukan password login biasa), setelah mengaktifkan Verifikasi 2 Langkah.

Atur environment variables berikut di komputer atau dashboard hosting:
- `MAIL_USERNAME` = alamat Gmail pengirim yang kamu gunakan untuk SMTP.
- `MAIL_PASSWORD` = Gmail App Password 16 karakter.
- `MAIL_SENDER` = alamat pengirim (opsional; biasanya sama dengan MAIL_USERNAME).
- `FLASK_SECRET_KEY` = teks acak panjang untuk secret key aplikasi.

Catatan: Gmail SMTP mengirim email melalui akun yang kamu konfigurasikan. Untuk praktik yang lebih aman, gunakan akun pengirim khusus dan jangan bagikan App Password.

## Deploy online dengan GitHub + Render
GitHub Pages tidak menjalankan backend Flask. Gunakan GitHub untuk menyimpan kode, lalu deploy repository ini sebagai **Web Service** di Render:
1. Buat repository GitHub dan unggah seluruh isi folder project.
2. Di Render, pilih New → Web Service, lalu hubungkan repository.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Tambahkan environment variables di Render seperti daftar di atas.
6. Deploy. Gunakan URL yang diberikan Render untuk dibagikan.

## Catatan privasi
Formulir meminta nama dan email pengunjung. Beri tahu pengunjung bahwa data mereka akan dikirim ke email pembuat website. Jangan meminta data sensitif. Aplikasi ini mengirim data melalui email dan tidak membuat database.

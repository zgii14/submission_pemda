# Submission Dicoding Fundamental Pemrosesan Data

Proyek ini merupakan bagian dari submission kelas **Fundamental Pemrosesan Data** di Dicoding. Proyek ini melakukan proses ETL (Extract, Transform, Load) terhadap data produk fashion dari situs [Fashion Studio Dicoding](https://fashion-studio.dicoding.dev/). Data diambil dari halaman 1 hingga 50, kemudian dibersihkan dan disimpan ke berbagai tujuan.

## Struktur Proyek

```
.
├── main.py
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── products.csv
└── README.md

```

## Fitur

- **Extract**: Mengambil data produk dari situs menggunakan `requests` dan `BeautifulSoup`.
- **Transform**: Membersihkan dan memformat data menggunakan `pandas`.
- **Load**: Menyimpan data hasil scraping ke:
  - File CSV (`products.csv`)
  - Google Sheets ([Link Spreadsheet](https://docs.google.com/spreadsheets/d/1rYM8cQNzgPJ8Eu1Jt_sP_XuEKAONa3hYKgAxWiaw6JE/edit?usp=sharing))
  - PostgreSQL Database

## Cara Menjalankan

### Jalankan Proses ETL

```bash
python main.py
````

### Jalankan Unit Test

```bash
python -m unittest discover tests
```

### Jalankan Test Coverage

```bash
coverage run -m unittest discover tests
coverage report -m
```

## Konfigurasi Database

Edit bagian `simpan_ke_postgresql()` di `utils/load.py` agar sesuai dengan konfigurasi lokal Anda:

```python
username = 'postgres'
password = 'rozagiro12'
host = 'localhost'
port = '5432'
database = 'product_db'
```

## Autentikasi Google Sheets

Pastikan Anda memiliki file `key_api.json` di direktori utama sebagai kredensial akses ke Google Sheets API.
Akan saya lampirkan di google drive. Berikut Link :
```
https://drive.google.com/drive/folders/1PVgT-wA9NvOTsvcWFvQdcUuI7rkHXnBS?usp=sharing
```
## Penulis

* 🧑 Nama: Muhammad Rozagi
* 📧 Email: [muhammadrozagi09@gmail.com](mailto:muhammadrozagi09@gmail.com)



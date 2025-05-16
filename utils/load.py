import os
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
def simpan_ke_csv(df, nama_file="products.csv"):
    """Simpan DataFrame ke file CSV."""
    df.to_csv(nama_file, index=False)
    print(f"✅ Data berhasil disimpan ke {nama_file}")

def simpan_ke_google_sheets(df, spreadsheet_id, range_sheet):
    """Simpan DataFrame ke Google Sheets."""
    if not os.path.exists('key_api.json'):
        print("❌ File key_api.json tidak ditemukan, lewati upload ke Google Sheets.")
        return

    try:
        creds = Credentials.from_service_account_file('key_api.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_sheet,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"✅ Data berhasil disimpan di Google Sheets pada {range_sheet}")

    except Exception as e:
        print(f"❌ Gagal simpan ke Google Sheets: {e}")

def simpan_ke_postgresql(data_frame, table_name='products'):
    """Menyimpan DataFrame ke PostgreSQL database."""
    try:
        # Ganti info berikut dengan konfigurasi PostgreSQL yang sesuai
        username = 'postgres'
        password = 'rozagiro12'
        host = 'localhost'
        port = '5432'
        database = 'product_db'

        # Buat koneksi engine SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        # Menyimpan DataFrame ke dalam tabel PostgreSQL (mengganti jika tabel sudah ada)
        data_frame.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Data berhasil disimpan ke tabel PostgreSQL '{table_name}'.")

    except Exception as e:
        print(f"❌Gagal menyimpan data ke PostgreSQL: {e}")
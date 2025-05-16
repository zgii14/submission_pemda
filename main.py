from utils.extract import ambil_data_produk
from utils.transform import bersihkan_dan_ubah
from utils.load import simpan_ke_csv, simpan_ke_google_sheets , simpan_ke_postgresql

def main():
    base_url = 'https://fashion-studio.dicoding.dev/'
    all_products = []

    print(f"Memulai scraping halaman utama: {base_url}")
    try:
        produk = ambil_data_produk(base_url)
        all_products.extend(produk)
    except Exception as e:
        print(f"❌ Gagal scraping halaman utama: {e}")

    for halaman in range(2, 51):
        url_halaman = f"{base_url}page{halaman}"
        print(f"Scraping halaman {halaman}: {url_halaman}")
        try:
            produk = ambil_data_produk(url_halaman)
            all_products.extend(produk)
        except Exception as e:
            print(f"❌ Gagal scraping halaman {halaman}: {e}")

    if not all_products:
        print("❌ Tidak ada produk yang berhasil di-scrape. Program dihentikan.")
        return

    data_bersih = bersihkan_dan_ubah(all_products)

    simpan_ke_csv(data_bersih)
    simpan_ke_google_sheets(
        data_bersih,
        spreadsheet_id='1rYM8cQNzgPJ8Eu1Jt_sP_XuEKAONa3hYKgAxWiaw6JE',
        range_sheet='Sheet1!A2'
    )
    simpan_ke_postgresql(data_bersih)
    print("✅ Semua data berhasil disimpan.")

if __name__ == "__main__":
    main()

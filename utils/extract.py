import requests
from bs4 import BeautifulSoup

def ambil_data_produk(url: str) -> list:
    """Ambil daftar produk dari halaman web."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise Exception(f"Gagal mengakses {url}: {err}")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        produk_list = []

        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            print(f"Tidak ada produk ditemukan di halaman {url}")

        for card in cards:
            title = card.find('h3', class_='product-title')
            price = card.find('div', class_='price-container')
            rating = card.find('p', string=lambda t: t and 'Rating' in t)
            colors = card.find('p', string=lambda t: t and 'Colors' in t)
            size = card.find('p', string=lambda t: t and 'Size' in t)
            gender = card.find('p', string=lambda t: t and 'Gender' in t)

            produk = {
                'title': title.text.strip() if title else 'Unknown Title',
                'price': price.text.strip() if price else 'Price Not Available',
                'rating': rating.text.strip() if rating else 'No Rating',
                'colors': colors.text.strip() if colors else 'No Color Info',
                'size': size.text.strip() if size else 'No Size Info',
                'gender': gender.text.strip() if gender else 'No Gender Info',
            }

            produk_list.append(produk)

        print(f"{len(produk_list)} produk berhasil diambil dari {url}")
        return produk_list

    except Exception as e:
        raise Exception(f"Kesalahan saat parsing HTML: {e}")

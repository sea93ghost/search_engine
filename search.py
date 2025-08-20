import requests
from openpyxl import Workbook
# Masukkan API Key Anda (daftar gratis di https://newsapi.org)
API_KEY = "6acfa02130c541bbac83ce7babb999ff"
BASE_URL = "https://newsapi.org/v2/everything"
import requests

def cari_berita(keyword, jumlah=50):
    params = {
        "q": keyword,
        "apiKey": API_KEY,
        "language": "id",  # berita bahasa Indonesia
        "sortBy": "publishedAt",
        "pageSize": jumlah
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print("Gagal mengambil data:", data)
        return []

    hasil = []
    for artikel in data["articles"]:
        hasil.append([
            artikel["title"],          # Judul
            artikel["source"]["name"], # Sumber
            artikel["url"],            # Link
            artikel["publishedAt"]     # Tanggal
        ])
    return hasil

def simpan_excel(berita, filename="hasil_berita.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Berita"

    # Header
    ws.append(["Judul", "Sumber", "URL", "Tanggal"])

    # Isi data
    for row in berita:
        ws.append(row)

    wb.save(filename)
    print(f"Hasil pencarian berhasil disimpan ke: {filename}")

# Contoh penggunaan
if __name__ == "__main__":
    keyword = input("Masukkan keyword pencarian: ")
    berita = cari_berita(keyword, jumlah=20)

    if berita:
        print(f"\nDitemukan {len(berita)} berita. Menyimpan ke Excel...\n")
        simpan_excel(berita)

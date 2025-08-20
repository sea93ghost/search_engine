import requests
from openpyxl import Workbook
# Masukkan API Key Anda (daftar gratis di https://newsapi.org)
API_KEY = "6acfa02130c541bbac83ce7babb999ff"
BASE_URL = "https://newsapi.org/v2/everything"
def cari_berita(keyword, jumlah=10):
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
        print(f"Gagal mengambil data untuk '{keyword}':", data)
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

def simpan_excel_multi(keyword_list, jumlah=10, filename="hasil_multi_keyword.xlsx"):
    wb = Workbook()
    wb.remove(wb.active)  # hapus sheet default

    for keyword in keyword_list:
        berita = cari_berita(keyword.strip(), jumlah)
        if not berita:
            continue

        # Buat sheet untuk keyword (maks 31 karakter sesuai batas Excel)
        sheet_name = keyword[:31]
        ws = wb.create_sheet(title=sheet_name)

        # Header
        ws.append(["Judul", "Sumber", "URL", "Tanggal"])

        # Isi data
        for row in berita:
            ws.append(row)

        print(f"Keyword '{keyword}' → {len(berita)} berita ditambahkan ke sheet '{sheet_name}'")

    wb.save(filename)
    print(f"\n✅ Semua hasil pencarian berhasil disimpan ke: {filename}")

# Contoh penggunaan
if __name__ == "__main__":
    keywords = input("Masukkan keyword pencarian (pisahkan dengan koma): ")
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    
    if keyword_list:
        simpan_excel_multi(keyword_list, jumlah=20)

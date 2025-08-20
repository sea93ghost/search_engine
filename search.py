import requests
from openpyxl import Workbook, load_workbook
import os
import schedule
import time
from datetime import datetime

# Masukkan API Key Anda dari https://newsapi.org
API_KEY = "6acfa02130c541bbac83ce7babb999ff"
BASE_URL = "https://newsapi.org/v2/everything"
FILENAME = "hasil_berita_harian.xlsx"

KEYWORDS = ["Jokowi", "Pemilu 2025", "Teknologi AI"]  # daftar keyword tetap

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
        print(f"Gagal ambil data untuk '{keyword}':", data)
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

def simpan_excel_harian(keyword_list, jumlah=10):
    # Jika file sudah ada → buka, kalau belum buat baru
    if os.path.exists(FILENAME):
        wb = load_workbook(FILENAME)
    else:
        wb = Workbook()
        wb.remove(wb.active)

    tanggal_sheet = datetime.now().strftime("%Y-%m-%d")

    for keyword in keyword_list:
        berita = cari_berita(keyword.strip(), jumlah)
        if not berita:
            continue

        # Nama sheet gabungan: keyword + tanggal (maks 31 karakter)
        sheet_name = (keyword[:20] + "_" + tanggal_sheet)[:31]

        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(title=sheet_name)
            ws.append(["Judul", "Sumber", "URL", "Tanggal"])

        for row in berita:
            ws.append(row)

        print(f"[{tanggal_sheet}] Keyword '{keyword}' → {len(berita)} berita ditambahkan ke sheet '{sheet_name}'")

    wb.save(FILENAME)
    print(f"✅ Data berita tersimpan ke {FILENAME}\n")

def job():
    print(f"\n⏳ Menjalankan update berita otomatis ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    simpan_excel_harian(KEYWORDS, jumlah=20)

if __name__ == "__main__":
    # Jadwalkan setiap hari jam 07:00
    schedule.every().day.at("07:00").do(job)

    print("Scheduler aktif ✅ (update berita jam 07:00 setiap hari)")
    while True:
        schedule.run_pending()
        time.sleep(30)

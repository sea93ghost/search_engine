import requests
import schedule
import time
from datetime import datetime, timedelta

# Ganti dengan API Key Anda
API_KEY = "6acfa02130c541bbac83ce7babb999ff"
BASE_URL = "https://newsapi.org/v2/everything"
KEYWORDS = ["oknum marinir", "oknum tni al", "oknum tni", "oknum aparat"]  # bisa pakai spasi

def cari_berita(keyword, jumlah=10):
    waktu_sekarang = datetime.utcnow()
    waktu_24jam = waktu_sekarang - timedelta(hours=24)

    params = {
        "q": keyword,
        "apiKey": API_KEY,
        "language": "id",
        "sortBy": "publishedAt",
        "pageSize": jumlah,
        "from": waktu_24jam.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print(f"Gagal ambil data untuk '{keyword}': {data.get('message', '')}")
        return []

    hasil = []
    for artikel in data.get("articles", []):
        hasil.append([
            artikel.get("title", "—"),
            artikel.get("source", {}).get("name", "—"),
            artikel.get("url", "—"),
            artikel.get("publishedAt", "—")
        ])
    return hasil

def job():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏳ Update berita otomatis ({now}), menampilkan berita 24 jam terakhir:")

    for keyword in KEYWORDS:
        berita = cari_berita(keyword, jumlah=10)
        if not berita:
            print(f"\n⚠  Tidak ada berita untuk keyword: '{keyword}' dalam 24 jam terakhir.")
            continue

        print(f"\n📌 Keyword: {keyword} → {len(berita)} berita:")
        for idx, (judul, sumber, url, tanggal) in enumerate(berita, start=1):
            print(f"{idx}. {judul}")
            print(f"   Sumber : {sumber}")
            print(f"   Link   : {url}")
            print(f"   Tanggal: {tanggal}")

if __name__ == "__main__":
    schedule.every(1).minutes.do(job)
    print("Scheduler aktif ✅ (update setiap menit, tampil di terminal saja)")
    while True:
        schedule.run_pending()
        time.sleep(20)

import feedparser
import schedule
import time
from datetime import datetime
import urllib.parse

# Daftar keyword yang ingin dipantau
KEYWORDS = ["oknum polisi", "pemilu 2025", "teknologi AI"]

def cari_berita(keyword):
    # Buat URL RSS berdasarkan keyword
    q = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={q}&hl=id&gl=ID&ceid=ID:id"

    feed = feedparser.parse(url)
    hasil = []

    for entry in feed.entries:
        hasil.append([
            entry.title,      # Judul berita
            entry.link,       # Link berita
            entry.published   # Tanggal terbit
        ])
    return hasil

def job():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏳ Update berita otomatis ({waktu})\n")

    for keyword in KEYWORDS:
        berita = cari_berita(keyword)
        if not berita:
            print(f"📌 Keyword: {keyword} → Tidak ada berita ditemukan\n")
            continue

        print(f"📌 Keyword: {keyword} (total {len(berita)} berita)\n")
        for i, artikel in enumerate(berita[:10], 1):  # tampilkan 10 berita pertama
            judul, url, tanggal = artikel
            print(f"{i}. {judul}")
            print(f"   Link   : {url}")
            print(f"   Tanggal: {tanggal}\n")

if __name__ == "__main__":
    # Jalankan tiap 30 menit
    schedule.every(30).minutes.do(job)

    print("Scheduler aktif ✅ (update berita tiap 30 menit, sumber: Google News RSS)")
    job()  # jalankan sekali saat start
    while True:
        schedule.run_pending()
        time.sleep(30)

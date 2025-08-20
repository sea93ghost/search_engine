import feedparser
import schedule
import time
from datetime import datetime
import urllib.parse

# Daftar keyword yang ingin dipantau
KEYWORDS = ["oknum tni", "oknum marinir", "marinir"]

# Set untuk menyimpan judul berita yang sudah tampil
sudah_muncul = set()

def cari_berita(keyword):
    q = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={q}&hl=id&gl=ID&ceid=ID:id"

    feed = feedparser.parse(url)
    hasil = []

    for entry in feed.entries:
        hasil.append([
            entry.title,
            entry.link,
            entry.published
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

            # Cek apakah judul ini baru
            if judul not in sudah_muncul:
                tanda = " [NEW] ✅"
                sudah_muncul.add(judul)
            else:
                tanda = ""

            print(f"{i}. {judul}{tanda}")
            print(f"   Link   : {url}")
            print(f"   Tanggal: {tanggal}\n")

if __name__ == "__main__":
    # Jalankan tiap 30 menit
    schedule.every(30).minutes.do(job)

    print("Scheduler aktif ✅ (update berita tiap 30 menit, highlight berita baru [NEW])")
    job()  # jalankan sekali saat start
    while True:
        schedule.run_pending()
        time.sleep(30)

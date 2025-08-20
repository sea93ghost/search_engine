import feedparser
import schedule
import time
from datetime import datetime, timedelta
import urllib.parse
import email.utils

# Daftar keyword yang ingin dipantau
KEYWORDS = ["oknum tni", "oknum marinir", "marinir"]

# Set untuk menyimpan judul berita yang sudah tampil
sudah_muncul = set()

def cari_berita(keyword):
    q = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={q}&hl=id&gl=ID&ceid=ID:id"

    feed = feedparser.parse(url)
    hasil = []
    batas_waktu = datetime.utcnow() - timedelta(hours=24)  # hanya 24 jam terakhir

    for entry in feed.entries:
        # Parse tanggal RSS (format RFC822)
        published_dt = datetime(*email.utils.parsedate(entry.published)[:6])

        if published_dt >= batas_waktu:  # hanya ambil berita 24 jam terakhir
            hasil.append([
                entry.title,
                entry.link,
                entry.published,
                published_dt
            ])
    return hasil

def job():
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏳ Update berita otomatis ({waktu})\n")

    for keyword in KEYWORDS:
        berita = cari_berita(keyword)
        if not berita:
            print(f"📌 Keyword: {keyword} → Tidak ada berita baru dalam 24 jam terakhir\n")
            continue

        print(f"📌 Keyword: {keyword} (ditemukan {len(berita)} berita dalam 24 jam terakhir)\n")
        for i, artikel in enumerate(berita[:10], 1):  # tampilkan 10 berita terbaru
            judul, url, published_str, published_dt = artikel

            # Cek apakah judul ini baru
            if judul not in sudah_muncul:
                tanda = " [NEW] ✅"
                sudah_muncul.add(judul)
            else:
                tanda = ""

            print(f"{i}. {judul}{tanda}")
            print(f"   Link   : {url}")
            print(f"   Tangg

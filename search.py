import requests

# Masukkan API Key Anda (daftar gratis di https://newsapi.org)
API_KEY = "6acfa02130c541bbac83ce7babb999ff"
BASE_URL = "https://newsapi.org/v2/everything"

def cari_berita(keyword, jumlah=5):
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
        hasil.append({
            "judul": artikel["title"],
            "sumber": artikel["source"]["name"],
            "url": artikel["url"],
            "tanggal": artikel["publishedAt"]
        })
    return hasil

# Contoh penggunaan
if __name__ == "__main__":
    keyword = input("Masukkan keyword pencarian: ")
    berita = cari_berita(keyword, jumlah=10)

    print("\n=== HASIL PENCARIAN BERITA ===")
    for i, b in enumerate(berita, 1):
        print(f"{i}. {b['judul']}")
        print(f"   Sumber : {b['sumber']}")
        print(f"   Link   : {b['url']}")
        print(f"   Tanggal: {b['tanggal']}\n")

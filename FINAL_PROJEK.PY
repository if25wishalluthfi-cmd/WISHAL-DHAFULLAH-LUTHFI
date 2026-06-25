"""
SISTEM MANAJEMEN INVENTORI GUDANG
=================================
Struktur Data:
  1. Hash Map (dict) -> Menyimpan data barang (Key: ID Barang) untuk CRUD O(1).
  2. Queue (list)    -> Antrean barang masuk (FIFO) untuk restock otomatis.
Fitur Tambahan:
  - Searching : Cari barang berdasarkan Nama (Linear Search).
  - Sorting   : Urutkan stok barang dari paling sedikit (Bubble Sort).
"""

import csv
import os

FILE_BARANG = "inventori.csv"

class InventoriGudang:
    def __init__(self):
        self.database = {}  # Hash Map untuk data barang {id_barang: {nama, stok, rak}}
        self.antrean_masuk = []  # Queue untuk antrean restock [id_barang, id_barang, ...]
        self.muat_data()

    def muat_data(self):
        if os.path.exists(FILE_BARANG):
            with open(FILE_BARANG, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.database[row["id_barang"]] = {
                        "nama": row["nama"],
                        "stok": int(row["stok"]),
                        "rak": row["rak"]
                    }

    def simpan_data(self):
        with open(FILE_BARANG, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id_barang", "nama", "stok", "rak"])
            for id_brg, info in self.database.items():
                writer.writerow([id_brg, info["nama"], info["stok"], info["rak"]])

    # --- OPERASI CRUD ---
    def tambah_barang(self):  # CREATE
        print("\n--- TAMBAH BARANG BARU ---")
        id_brg = input("Masukkan ID Barang: ").strip()
        if id_brg in self.database:
            print(" ID Barang sudah ada!")
            return
        nama = input("Masukkan Nama Barang: ").strip()
        try:
            stok = int(input("Masukkan Jumlah Stok Awal: "))
        except ValueError:
            print(" Stok harus berupa angka.")
            return
        rak = input("Masukkan Lokasi Rak: ").strip()

        self.database[id_brg] = {"nama": nama, "stok": stok, "rak": rak}
        self.simpan_data()
        print(f"✅ Barang '{nama}' berhasil ditambahkan ke database.")

    def lihat_semua_barang(self):  # READ
        print("\n--- DAFTAR SEMUA BARANG GUDANG ---")
        if not self.database:
            print("Gudang kosong.")
            return
        print(f"{'ID':<8}{'Nama Barang':<20}{'Stok':<8}{'Lokasi Rak':<10}")
        print("-" * 46)
        for id_brg, info in self.database.items():
            print(f"{id_brg:<8}{info['nama']:<20}{info['stok']:<8}{info['rak']:<10}")

    def update_stok_manual(self):  # UPDATE
        print("\n--- UPDATE STOK MANAUL ---")
        id_brg = input("Masukkan ID Barang: ").strip()
        if id_brg not in self.database:
            print(" ID Barang tidak ditemukan.")
            return
        try:
            stok_baru = int(input("Masukkan Jumlah Stok Baru: "))
        except ValueError:
            print(" Stok harus berupa angka.")
            return
        self.database[id_brg]["stok"] = stok_baru
        self.simpan_data()
        print(f"✅ Stok ID {id_brg} berhasil diperbarui menjadi {stok_baru}.")

    def hapus_barang(self):  # DELETE
        print("\n--- HAPUS BARANG FROM DATABASE ---")
        id_brg = input("Masukkan ID Barang yang akan dihapus: ").strip()
        if id_brg in self.database:
            nama = self.database[id_brg]["nama"]
            del self.database[id_brg]
            self.simpan_data()
            print(f" Barang '{nama}' berhasil dihapus.")
        else:
            print(" ID Barang tidak ditemukan.")

    # --- FITUR STRUKTUR DATA (QUEUE, SEARCHING, SORTING) ---
    def tambah_ke_antrean(self):  # Enqueue
        id_brg = input("Masukkan ID Barang untuk antrean restock: ").strip()
        if id_brg not in self.database:
            print(" Daftarkan barang terlebih dahulu di Menu 1.")
            return
        self.antrean_masuk.append(id_brg)
        print(f" Barang '{self.database[id_brg]['nama']}' masuk antrean restock nomor {len(self.antrean_masuk)}.")

    def proses_antrean_restock(self):  # Dequeue
        if not self.antrean_masuk:
            print("\n Tidak ada antrean restock saat ini.")
            return
        id_brg = self.antrean_masuk.pop(0)  # FIFO
        try:
            jumlah = int(input(f"Masukkan jumlah barang masuk untuk '{self.database[id_brg]['nama']}': "))
        except ValueError:
            print(" Harus angka. Proses dibatalkan.")
            self.antrean_masuk.insert(0, id_brg) # Kembalikan ke antrean terdepan jika gagal
            return
        self.database[id_brg]["stok"] += jumlah
        self.simpan_data()
        print(f" Restock berhasil. Stok terbaru '{self.database[id_brg]['nama']}': {self.database[id_brg]['stok']}")

    def cari_barang(self):  # Linear Searching
        print("\n--- CARI BARANG ---")
        keyword = input("Masukkan potongan nama barang: ").lower()
        ditemukan = False
        for id_brg, info in self.database.items():
            if keyword in info["nama"].lower():
                print(f"[Ketemu] ID: {id_brg} | Nama: {info['nama']} | Stok: {info['stok']} | Rak: {info['rak']}")
                ditemukan = True
        if not ditemukan:
            print(" Barang tidak ditemukan.")

    def laporan_stok_kritis(self):  # Bubble Sorting
        print("\n--- LAPORAN STOK PALING SEDIKIT (SORTED) ---")
        if not self.database:
            print("Tidak ada data.")
            return
        # Konversi dict ke list untuk disorting
        daftar_barang = []
        for id_brg, info in self.database.items():
            daftar_barang.append({"id": id_brg, "nama": info["nama"], "stok": info["stok"]})
        
        # Algoritma Bubble Sort berdasarkan Stok terkecil
        n = len(daftar_barang)
        for i in range(n):
            for j in range(0, n - i - 1):
                if daftar_barang[j]["stok"] > daftar_barang[j+1]["stok"]:
                    daftar_barang[j], daftar_barang[j+1] = daftar_barang[j+1], daftar_barang[j]
        
        for item in daftar_barang:
            print(f"Stok: {item['stok']:<5} | ID: {item['id']:<5} | Nama: {item['nama']}")

def main():
    app = InventoriGudang()
    while True:
        print("\n=======================================")
        print("     SISTEM INVENTORI GUDANG (.CSV)    ")
        print("=======================================")
        print("1. Tambah Barang Baru (Create)")
        print("2. Lihat Semua Barang (Read)")
        print("3. Update Stok Manual (Update)")
        print("4. Hapus Barang (Delete)")
        print("5. Masukkan ke Antrean Restock (Queue)")
        print("6. Proses Antrean Terdepan (Dequeue)")
        print("7. Cari Barang (Searching)")
        print("8. Urutkan Stok Terkecil (Sorting)")
        print("0. Keluar")
        
        pilihan = input("Pilih Menu: ").strip()
        if pilihan == "1": app.tambah_barang()
        elif pilihan == "2": app.lihat_semua_barang()
        elif pilihan == "3": app.update_stok_manual()
        elif pilihan == "4": app.hapus_barang()
        elif pilihan == "5": app.tambah_ke_antrean()
        elif pilihan == "6": app.proses_antrean_restock()
        elif pilihan == "7": app.cari_barang()
        elif pilihan == "8": app.laporan_stok_kritis()
        elif pilihan == "0":
            print("Keluar dari program. Terima kasih! 👋")
            break
        else:
            print(" Pilihan tidak valid.")

if __name__ == "__main__":
    main()
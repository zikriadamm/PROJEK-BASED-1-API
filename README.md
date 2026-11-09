# Travel Expense Tracker & Currency Converter RESTful API
**Evaluasi Sub-CPMK 4 — Project Based Learning (PBL)**  
Mata Kuliah: **Rekayasa API (F09252013)**  
Kelompok: **Kelompok 3**

## Anggota Kelompok
1. **Lidiya** — `F5512530118`
2. **Tabita Creaselia Belicia Theona** — `F5512520086`
3. **Muhammad Zikri Adam** — `F5512530117`
4. **Trista Sheryl Lambei** — `F5512530106`

---

## 1. Arsitektur Sistem
```text
[ Client Console CLI (client.js) ]
            │
            │ (HTTP Request / Response)
            ▼
[ Server REST API Kelompok (server.js - module http) ]
      │                                       │
      ▼ (fs/promises)                         ▼ (fetch ke internet)
[ data/expenses.json ]                  [ ExchangeRate-API (Valas Live) ]
```

---

## 2. Cara Menjalankan Proyek untuk Demo Kelas

Buka **dua jendela terminal terpisah**:

### Terminal 1: Menjalankan Server API
```bash
cd "d:\Tugas semester 3\API\PROJEK BASED 1 API"
node server.js
```
*Server akan mencetak identitas kelompok di baris paling atas dan berjalan di port `3000`.*

### Terminal 2: Menjalankan Client Console Interaktif
```bash
cd "d:\Tugas semester 3\API\PROJEK BASED 1 API"
node client.js
```
*Client console akan menampilkan antarmuka menu CLI bernomor 0-7, dapat memanggil seluruh endpoint, memfilter pengeluaran, menampilkan kalkulasi kurs live IDR, ringkasan risiko anggaran, dan menangani error secara ramah tanpa stack trace.*

---

## 3. Koleksi Pengujian API

### A. Pengujian via Bruno (Direkomendasikan)
Folder koleksi Bruno asli siap pakai tersedia di:  
`bruno-collection/`

**Cara membuka di Bruno:**
1. Buka aplikasi **Bruno**.
2. Klik **Open Collection** (atau `Ctrl + O`).
3. Pilih folder: `d:\Tugas semester 3\API\PROJEK BASED 1 API\bruno-collection`.
4. Pilih environment **Local** di pojok kanan atas Bruno.
5. Anda dapat langsung menjalankan seluruh request dari nomor `1` sampai `11` dan mengambil screenshot responnya.

### B. Pengujian via Postman
Koleksi lengkap Postman tersedia di:  
`postman/PBL1_Travel_Expense_API.postman_collection.json`

Cukup buka Postman -> **Import** -> pilih berkas JSON di atas.  
Koleksi memuat 11 skenario pengujian (sukses & gagal) untuk memenuhi ketentuan penilaian.

---

## 4. Berkas Laporan Proyek
Berkas laporan proyek siap cetak/ekspor PDF tersedia di:  
`Laporan_Proyek_PBL1_Rekayasa_API.docx`  
*(Disusun sesuai format akademik 8 bab dengan margin 4-4-3-3 cm, Times New Roman 12 pt, dan spasi 1.5).*

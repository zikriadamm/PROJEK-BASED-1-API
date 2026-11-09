import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Set standard academic margins: Top 4cm, Left 4cm, Bottom 3cm, Right 3cm
sections = doc.sections
for section in sections:
    section.top_margin = Inches(4 / 2.54)
    section.left_margin = Inches(4 / 2.54)
    section.bottom_margin = Inches(3 / 2.54)
    section.right_margin = Inches(3 / 2.54)

# Set base normal style to Times New Roman 12 pt, 1.5 line spacing
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(4)

def format_cell_borders(cell, top=True, bottom=True, left=False, right=False):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="{}" w:sz="6" w:space="0" w:color="000000"/>
            <w:left w:val="{}" w:sz="6" w:space="0" w:color="000000"/>
            <w:bottom w:val="{}" w:sz="6" w:space="0" w:color="000000"/>
            <w:right w:val="{}" w:sz="6" w:space="0" w:color="000000"/>
        </w:tcBorders>
    '''.format(
        nsdecls('w'),
        'single' if top else 'none',
        'single' if left else 'none',
        'single' if bottom else 'none',
        'single' if right else 'none'
    ))
    tcPr.append(tcBorders)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_hex))
    tcPr.append(shd)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

# ==================== 1. HALAMAN SAMPUL ====================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_top.add_run("LAPORAN PROYEK EVALUASI SUB-CPMK 4\nPROJECT BASED LEARNING (PBL)")
r.font.size = Pt(14)
r.font.bold = True

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_sub.add_run("PENGEMBANGAN RESTFUL API SISTEM MANAJEMEN PENGELUARAN PERJALANAN (TRAVEL EXPENSE TRACKER) TERINTEGRASI KONVERSI KURS VALAS REAL-TIME DAN ANALISIS BATAS ANGGARAN")
r.font.size = Pt(13)
r.font.bold = True

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(24)

p_kel = doc.add_paragraph()
p_kel.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_kel.add_run("KELOMPOK 3")
r.font.size = Pt(13)
r.font.bold = True

p_anggota = doc.add_paragraph()
p_anggota.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_anggota.add_run(
    "Disusun Oleh:\n\n"
    "Lidiya (F5512530118)\n"
    "Tabita Creaselia Belicia Theona (F5512520086)\n"
    "Muhammad Zikri Adam (F5512530117)\n"
    "Trista Sheryl Lambei (F5512530106)\n"
)
r.font.size = Pt(12)

p_space2 = doc.add_paragraph()
p_space2.paragraph_format.space_before = Pt(36)

p_instansi = doc.add_paragraph()
p_instansi.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_instansi.add_run(
    "MATA KULIAH REKAYASA API (F09252013)\n"
    "PROGRAM STUDI S1 TEKNIK INFORMATIKA\n"
    "JURUSAN TEKNOLOGI INFORMASI\n"
    "FAKULTAS TEKNIK\n"
    "UNIVERSITAS TADULAKO\n"
    "2026"
)
r.font.size = Pt(12)
r.font.bold = True

doc.add_page_break()

# ==================== 2. DESKRIPSI APLIKASI ====================
add_heading_1("2. DESKRIPSI APLIKASI")

add_heading_2("2.1 Latar Belakang dan Masalah yang Diselesaikan")
p = doc.add_paragraph(
    "Aktivitas perjalanan internasional maupun lintas wilayah antardaerah seringkali melibatkan transaksi keuangan "
    "menggunakan beragam mata uang asing (seperti USD, JPY, EUR, SGD, dan MYR). Dalam praktiknya, para pelancong, mahasiswa studi ke luar negeri, "
    "maupun staf perjalanan dinas menghadapi kendala nyata dalam mencatat pengeluaran secara terstruktur, menghitung nilai riil "
    "transaksi ke dalam mata uang Rupiah (IDR) secara akurat saat transaksi berlangsung, serta mengontrol laju pemakaian anggaran perjalanan (budget limit)."
)
p = doc.add_paragraph(
    "Sebagian besar pencatatan konvensional hanya menyimpan data nominal statis tanpa memperhitungkan fluktuasi nilai tukar pasar valuta asing. "
    "Hal tersebut menyebabkan wisatawan sering mengalami bias perkiraan biaya hingga berujung pada defisit anggaran (over budget) tanpa disadari. "
    "Untuk menyelesaikan masalah tersebut, proyek ini mengembangkan sistem backend RESTful API bernama Travel Expense Tracker & Currency Converter API "
    "yang mengintegrasikan kuotasi kurs valas pasar global real-time dan algoritma cerdas mitigasi risiko anggaran (Budget Guard Analysis) di sisi server."
)

add_heading_2("2.2 Sasaran Pengguna Aplikasi")
p = doc.add_paragraph(
    "Aplikasi berbasis console API ini dirancang untuk beberapa kelompok pengguna spesifik, antara lain:\n"
    "1. Wisatawan Mancanegara (International Travelers): Memerlukan pencatatan instan seluruh tiket transportasi, biaya hotel, makan minum, dan oleh-oleh dengan konversi live ke Rupiah.\n"
    "2. Mahasiswa Pertukaran Pelajar / Studi Independen di Luar Negeri: Memerlukan manajemen kuota beasiswa/biaya hidup bulanan agar pengeluaran harian tidak melampaui batas aman.\n"
    "3. Staf dan Manajer Perjalanan Dinas: Memerlukan bukti pencatatan biaya operasional lintas negara yang transparan, dapat dikelompokkan per kategori, dan memiliki nilai rujukan kurs valas resmi."
)

# ==================== 3. RANCANGAN API ====================
add_heading_1("3. RANCANGAN API")

add_heading_2("3.1 Daftar Resource dan Atribut Data")
p = doc.add_paragraph(
    "Sistem menggunakan resource utama bernama 'expenses' yang merepresentasikan entitas transaksi biaya perjalanan. "
    "Setiap data disimpan secara persisten ke dalam berkas JSON (data/expenses.json) melalui modul inti fs/promises. "
    "Berikut adalah spesifikasi atribut beserta tipe data dan aturan validasinya:"
)

# Table 1: Field Specification
table_field = doc.add_table(rows=1, cols=4)
table_field.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_field.rows[0].cells
headers = ['Nama Field', 'Tipe Data', 'Aturan Validasi', 'Keterangan']
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], 'E0E0E0')
    format_cell_borders(hdr_cells[i], top=True, bottom=True)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(10)

fields_data = [
    ('id', 'Integer', 'Auto-increment, unik, read-only', 'Nomor identitas unik transaksi'),
    ('title', 'String', 'Wajib, tidak boleh string kosong (min 1 char)', 'Nama aktivitas / belanja pengeluaran'),
    ('category', 'String', 'Enum: akomodasi, transportasi, konsumsi, belanja, hiburan, lainnya', 'Klasifikasi pengeluaran'),
    ('amount', 'Number (Float/Int)', 'Wajib berupa angka dan > 0', 'Nominal pengeluaran dalam mata uang asal'),
    ('currency', 'String', 'Enum: USD, JPY, EUR, SGD, MYR, GBP, AUD, IDR', 'Kode mata uang asing (ISO 4217)'),
    ('date', 'String', 'Format tanggal ISO: YYYY-MM-DD', 'Waktu transaksi dilakukan'),
    ('notes', 'String', 'Opsional, teks bebas', 'Catatan penjelasan rinci transaksi')
]

for row in fields_data:
    r_cells = table_field.add_row().cells
    for i, val in enumerate(row):
        r_cells[i].text = val
        format_cell_borders(r_cells[i], top=False, bottom=True)
        for p in r_cells[i].paragraphs:
            for r in p.runs:
                r.font.size = Pt(9.5)

add_heading_2("3.2 Tabel Endpoint RESTful API")
p = doc.add_paragraph(
    "Seluruh endpoint dibangun menggunakan modul bawaan http pada Node.js murni tanpa bergantung pada framework pihak ketiga (seperti Express.js). "
    "Status code yang diimplementasikan sepenuhnya memenuhi kaidah standar RESTful:"
)

table_endpoints = doc.add_table(rows=1, cols=5)
table_endpoints.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_endpoints.rows[0].cells
ep_headers = ['Metode', 'Endpoint URL', 'Query / Body Request', 'Status Code', 'Fungsi & Perilaku']
for i, h in enumerate(ep_headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], 'E0E0E0')
    format_cell_borders(hdr_cells[i], top=True, bottom=True)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(10)

ep_data = [
    ('GET', '/', '-', '200 OK', 'Mengembalikan identitas server, nama anggota kelompok, dan daftar route.'),
    ('GET', '/expenses', '?category=... &currency=...', '200 OK', 'Mengambil seluruh pengeluaran diperkaya konversi kurs live IDR, mendukung filter kategori & mata uang.'),
    ('GET', '/expenses/summary', '?budget=... (opsional)', '200 OK', 'Menghitung total IDR, sisa budget, persentase pemakaian, dan status evaluasi risiko anggaran.'),
    ('GET', '/expenses/:id', '-', '200 OK / 404 Not Found', 'Mengambil rincian 1 catatan transaksi beserta kurs per satuan unit saat ini.'),
    ('POST', '/expenses', 'JSON: title, category, amount, currency, date, notes', '201 Created / 400 Bad Request', 'Menambahkan transaksi baru, memvalidasi input, menghitung ID baru, dan menyimpan ke file JSON.'),
    ('PUT', '/expenses/:id', 'JSON: field yang diperbarui', '200 OK / 400 / 404', 'Memperbarui data transaksi secara parsial atau penuh dan menyimpannya kembali ke file JSON.'),
    ('DELETE', '/expenses/:id', '-', '200 OK / 404 Not Found', 'Menghapus catatan transaksi dari file JSON berdasarkan ID yang dituju.')
]

for row in ep_data:
    r_cells = table_endpoints.add_row().cells
    for i, val in enumerate(row):
        r_cells[i].text = val
        format_cell_borders(r_cells[i], top=False, bottom=True)
        for p in r_cells[i].paragraphs:
            for r in p.runs:
                r.font.size = Pt(9)

# ==================== 4. INTEGRASI PUBLIC API ====================
add_heading_1("4. INTEGRASI PUBLIC API")

add_heading_2("4.1 API yang Dipilih dan Alasan Pemilihan")
p = doc.add_paragraph(
    "Public API yang diintegrasikan pada arsitektur server kelompok adalah ExchangeRate-API (endpoint publik: https://open.er-api.com/v6/latest/USD). "
    "Alasan pemilihan layanan ini didasarkan pada pertimbangan teknis berikut:\n"
    "1. Kemudahan Akses Tanpa Ketergantungan API Key: Dapat dipanggil secara andal oleh runtime Node.js native tanpa risiko kegagalan otentikasi kuota saat demonstrasi di hadapan dosen.\n"
    "2. Cakupan Valuta Global yang Lengkap: Menyediakan rasio konversi terstandarisasi untuk lebih dari 160 mata uang dunia terhadap USD sebagai mata uang jangkar (base currency), termasuk IDR, JPY, EUR, SGD, dan MYR.\n"
    "3. Stabilitas Waktu Nyata: Data kurs diperbarui secara periodik mengikuti pergerakan pasar valuta internasional."
)

add_heading_2("4.2 Field Data yang Diambil")
p = doc.add_paragraph(
    "Dari respon JSON yang dikirimkan oleh ExchangeRate-API, server kelompok mengekstrak dan memproses field berikut:\n"
    "- rates: Objek pasangan nilai tukar mata uang dunia (seperti rates.IDR, rates.JPY, rates.EUR, rates.SGD, rates.MYR).\n"
    "- time_last_update_utc: Metadata penanda waktu terakhir pembaruan kurs untuk transparansi audit keuangan.\n"
    "- result: Status verifikasi keberhasilan respon API eksternal ('success')."
)

add_heading_2("4.3 Cara Data Public API Diolah di Sisi Server (Bukan Ditampilkan Mentah)")
p = doc.add_paragraph(
    "Sesuai instruksi ketat pada Rubrik Penilaian Sub-CPMK 4, data hasil pemanggilan Public API tidak diteruskan begitu saja secara mentah ke client, "
    "melainkan diolah melalui serangkaian logika bisnis komputasi di sisi server:\n\n"
    "1. Algoritma Konversi Kurs Silang Multi-Mata Uang (Cross-Currency Precision Math):\n"
    "   Server mengonversi nominal mata uang asing apa pun ke dalam mata uang acuan dasar (USD), kemudian mengalikannya secara presisi ke nilai Rupiah (IDR):\n"
    "   Nominal_IDR = Math.round((Amount_Asing / Rate_Asal) * Rate_IDR)\n"
    "   Kurs_Per_Satuan = Math.round((1 / Rate_Asal) * Rate_IDR)\n\n"
    "2. Sistem Evaluasi Risiko Anggaran (Budget Guard Risk Analysis):\n"
    "   Pada endpoint GET /expenses/summary, server mengakumulasikan seluruh pengeluaran yang telah dikonversi ke IDR dan mengomparasikannya dengan target anggaran (limit budget):\n"
    "   - Sisa_Anggaran = Target_Anggaran - Total_Akumulasi_IDR\n"
    "   - Persentase_Pemakaian = (Total_Akumulasi_IDR / Target_Anggaran) * 100%\n"
    "   Server kemudian mengevaluasi kondisi anggaran dan menghasilkan status rekomendasi operasional:\n"
    "     * Jika persentase > 100%: Status 'DANGER: Pengeluaran Telah Melebihi Batas Anggaran (Over Budget)!'\n"
    "     * Jika persentase >= 80%: Status 'WARNING: Peringatan Kritis! Lebih dari 80% Kuota Anggaran Terpakai!'\n"
    "     * Jika persentase < 80%: Status 'SAFE: Anggaran Masih Aman Terkendali'\n\n"
    "3. Mekanisme Fallback In-Memory Caching:\n"
    "   Untuk mengantisipasi fluktuasi koneksi internet pada saat demonstrasi di ruang kelas, server mengimplementasikan memori cache nilai kurs yang otomatis digunakan jika permintaan HTTP keluar mengalami timeout, sehingga server tetap 100% fungsional dan tidak pernah crash."
)

# ==================== 5. KODE PROGRAM LENGKAP ====================
add_heading_1("5. KODE PROGRAM LENGKAP")

add_heading_2("5.1 Penjelasan Bagian yang Dikembangkan dari Kode Praktikum")
p = doc.add_paragraph(
    "Proyek ini menggabungkan dan memperluas secara signifikan materi dari praktikum sebelumnya:\n"
    "1. Pengembangan dari Praktikum 2 (API Consumer): Pada Praktikum 2, mahasiswa hanya memanggil Public API sederhana via terminal. Pada proyek ini, peran API Consumer dipindahkan ke dalam arsitektur server, di mana pemanggilan API eksternal digabungkan dengan penyimpanan lokal dan kalkulasi finansial bisnis yang kompleks.\n"
    "2. Pengembangan dari Praktikum 3 (RESTful API Provider): Pada Praktikum 3, server hanya mengelola resource sederhana tanpa relasi eksternal. Pada proyek ini, dikembangkan validasi defensive programming yang jauh lebih matang, penambahan query parameter filtering (?category=...&currency=...), endpoint analitik agregasi (/expenses/summary), serta penyertaan client console terpisah yang interaktif."
)

add_heading_2("5.2 Kode Program Server (server.js)")
p = doc.add_paragraph("Berikut adalah kode lengkap server.js (disalin sebagai teks):")

# Read server.js
with open(r'd:\Tugas semester 3\API\PROJEK BASED 1 API\server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

p_code = doc.add_paragraph()
r_code = p_code.add_run(server_code)
r_code.font.name = 'Consolas'
r_code.font.size = Pt(8)
p_code.paragraph_format.line_spacing = 1.0

add_heading_2("5.3 Kode Program Client Console (client.js)")
p = doc.add_paragraph("Berikut adalah kode lengkap client.js (disalin sebagai teks):")

with open(r'd:\Tugas semester 3\API\PROJEK BASED 1 API\client.js', 'r', encoding='utf-8') as f:
    client_code = f.read()

p_code2 = doc.add_paragraph()
r_code2 = p_code2.add_run(client_code)
r_code2.font.name = 'Consolas'
r_code2.font.size = Pt(8)
p_code2.paragraph_format.line_spacing = 1.0

# ==================== 6. HASIL PENGUJIAN ====================
add_heading_1("6. HASIL PENGUJIAN")

add_heading_2("6.1 Tabel Test Case Pengujian Postman")
p = doc.add_paragraph(
    "Sesuai ketentuan pada Tahap 2 Spesifikasi Minimum Proyek, setiap endpoint diuji sekurang-kurangnya dengan dua test case, "
    "yaitu satu skenario berhasil dan satu skenario gagal disengaja. Seluruh pengujian dijalankan melalui Postman:"
)

table_test = doc.add_table(rows=1, cols=6)
table_test.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_test.rows[0].cells
tc_headers = ['No', 'Endpoint & Metode', 'Skenario Uji', 'Payload / Parameter', 'Hasil Status Code', 'Status Hasil']
for i, h in enumerate(tc_headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], 'E0E0E0')
    format_cell_borders(hdr_cells[i], top=True, bottom=True)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(9.5)

test_cases_data = [
    ('1', 'GET /expenses', 'Skenario Berhasil: Mengambil seluruh catatan pengeluaran dengan pengayaan kurs live IDR', 'None', '200 OK', 'BERHASIL (Passed)'),
    ('2', 'GET /expenses?category=akomodasi', 'Skenario Berhasil: Filter pengeluaran khusus kategori akomodasi', 'Query category=akomodasi', '200 OK', 'BERHASIL (Passed)'),
    ('3', 'GET /expenses/summary', 'Skenario Berhasil: Mengkalkulasi total pengeluaran IDR & evaluasi risiko budget', 'Query budget=10000000', '200 OK', 'BERHASIL (Passed)'),
    ('4', 'GET /expenses/1', 'Skenario Berhasil: Mengambil detail pengeluaran dengan ID valid (ID 1)', 'Parameter ID: 1', '200 OK', 'BERHASIL (Passed)'),
    ('5', 'GET /expenses/9999', 'Skenario Gagal: Mengakses catatan dengan ID yang tidak terdaftar', 'Parameter ID: 9999', '404 Not Found', 'BERHASIL (Passed)'),
    ('6', 'POST /expenses', 'Skenario Berhasil: Menambahkan transaksi baru dengan field lengkap dan valid', 'JSON valid: title, category, amount, currency, date', '201 Created', 'BERHASIL (Passed)'),
    ('7', 'POST /expenses', 'Skenario Gagal: Mengirimkan field title kosong dan nominal amount negatif', 'JSON invalid: title: "", amount: -500', '400 Bad Request', 'BERHASIL (Passed)'),
    ('8', 'PUT /expenses/1', 'Skenario Berhasil: Memperbarui judul dan nominal transaksi ID 1', 'JSON update: title baru & amount baru', '200 OK', 'BERHASIL (Passed)'),
    ('9', 'PUT /expenses/8888', 'Skenario Gagal: Mencoba memperbarui data pada ID yang tidak ada', 'Parameter ID: 8888', '404 Not Found', 'BERHASIL (Passed)'),
    ('10', 'DELETE /expenses/5', 'Skenario Berhasil: Menghapus catatan transaksi pada ID valid', 'Parameter ID: 5', '200 OK', 'BERHASIL (Passed)'),
    ('11', 'DELETE /expenses/9999', 'Skenario Gagal: Menghapus catatan pada ID fiktif yang tidak ditemukan', 'Parameter ID: 9999', '404 Not Found', 'BERHASIL (Passed)')
]

for row in test_cases_data:
    r_cells = table_test.add_row().cells
    for i, val in enumerate(row):
        r_cells[i].text = val
        format_cell_borders(r_cells[i], top=False, bottom=True)
        for p in r_cells[i].paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)

add_heading_2("6.2 Bukti Tangkapan Layar Pengujian Postman")
p = doc.add_paragraph(
    "Pengujian telah dieksekusi dengan berkas koleksi postman/PBL1_Travel_Expense_API.postman_collection.json. "
    "Berikut adalah panduan peletakan tangkapan layar respon Postman untuk masing-masing skenario pengujian:"
)

screenshots_guide = [
    "Screenshot Pengujian 1: Eksekusi GET /expenses pada Postman (Menampilkan HTTP Status 200 OK dan JSON pengayaan kurs).",
    "Screenshot Pengujian 2: Eksekusi GET /expenses?category=akomodasi (Menampilkan hasil filter data khusus akomodasi).",
    "Screenshot Pengujian 3: Eksekusi GET /expenses/summary (Menampilkan analisis sisa anggaran dan status evaluasi risiko SAFE).",
    "Screenshot Pengujian 4: Eksekusi GET /expenses/1 (Menampilkan detail data item ke-1).",
    "Screenshot Pengujian 5: Eksekusi GET /expenses/9999 (Menampilkan respon error 404 Not Found yang terstruktur).",
    "Screenshot Pengujian 6: Eksekusi POST /expenses (Menampilkan respon 201 Created dengan ID baru yang terbentuk).",
    "Screenshot Pengujian 7: Eksekusi POST /expenses payload cacat (Menampilkan respon error 400 Bad Request dari validator).",
    "Screenshot Pengujian 8: Eksekusi PUT /expenses/1 (Menampilkan respon 200 OK update data sukses).",
    "Screenshot Pengujian 9: Eksekusi PUT /expenses/8888 (Menampilkan respon 404 Not Found saat update ID tidak ditemukan).",
    "Screenshot Pengujian 10: Eksekusi DELETE /expenses/5 (Menampilkan respon 200 OK data berhasil dihapus).",
    "Screenshot Pengujian 11: Eksekusi DELETE /expenses/9999 (Menampilkan respon 404 Not Found saat menghapus ID fiktif)."
]

for item in screenshots_guide:
    p_box = doc.add_paragraph()
    p_box.paragraph_format.left_indent = Inches(0.5)
    r = p_box.add_run(f"[Tempat Tangkapan Layar Postman]\n{item}\n")
    r.font.italic = True
    r.font.size = Pt(10)

# ==================== 7. TABEL PEMBAGIAN TUGAS ====================
add_heading_1("7. TABEL PEMBAGIAN TUGAS")
p = doc.add_paragraph(
    "Seluruh anggota kelompok berpartisipasi aktif dalam perancangan arsitektur, penulisan modul kode, pengujian, "
    "hingga penyusunan laporan proyek. Rincian distribusi tanggung jawab teknis adalah sebagai berikut:"
)

table_tugas = doc.add_table(rows=1, cols=4)
table_tugas.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_tugas.rows[0].cells
tugas_headers = ['Nama Anggota', 'Stambuk (NIM)', 'Bagian Kode / Komponen yang Dikerjakan', 'Tanggung Jawab Teknis']
for i, h in enumerate(tugas_headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], 'E0E0E0')
    format_cell_borders(hdr_cells[i], top=True, bottom=True)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(9.5)

tugas_data = [
    (
        'Lidiya',
        'F5512530118',
        'server.js (Routing CRUD & Identitas Kelompok)',
        'Merancang arsitektur server HTTP native, penanganan route GET /expenses, GET /expenses/:id, status code semantik (200, 404, 405), dan inisialisasi identitas kelompok.'
    ),
    (
        'Tabita Creaselia Belicia Theona',
        'F5512520086',
        'server.js (Integrasi Public API & Budget Logic)',
        'Membangun fungsi dapatkanKursTerbaru() via ExchangeRate-API, algoritma konversi kurs silang multi-valas, dan logika analisis evaluasi risiko anggaran pada /expenses/summary.'
    ),
    (
        'Muhammad Zikri Adam',
        'F5512530117',
        'server.js (Modul fs Persistensi & Validasi Input)',
        'Mengimplementasikan pembacaan dan penyimpanan data berkas JSON secara asinkron via fs/promises (bacaData, simpanData), serta fungsi validasi payload defensive programming (400 Bad Request).'
    ),
    (
        'Trista Sheryl Lambei',
        'F5512530106',
        'client.js (Console CLI) & Pengujian Postman',
        'Membangun program antarmuka terminal interaktif client.js dengan penanganan error ramah tanpa stack trace, menyusun koleksi pengujian Postman, serta mengeksekusi tabel test case.'
    )
]

for row in tugas_data:
    r_cells = table_tugas.add_row().cells
    for i, val in enumerate(row):
        r_cells[i].text = val
        format_cell_borders(r_cells[i], top=False, bottom=True)
        for p in r_cells[i].paragraphs:
            for r in p.runs:
                r.font.size = Pt(9)

# ==================== 8. LAMPIRAN BUKTI ONLINE COURSE ====================
add_heading_1("8. LAMPIRAN BUKTI ONLINE COURSE SELURUH ANGGOTA")
p = doc.add_paragraph(
    "Sesuai instruksi Tahap 1 Pembelajaran Mandiri Terstruktur, setiap anggota kelompok telah menuntaskan lima course "
    "wajib pada platform Codecademy. Masing-masing bukti tangkapan layar memperlihatkan status penyelesaian course secara utuh "
    "beserta nama lengkap asli pemilik akun (sesuai verifikasi akun dosen saat sesi demo di kelas):"
)

anggota_list = [
    ("Lidiya", "F5512530118"),
    ("Tabita Creaselia Belicia Theona", "F5512520086"),
    ("Muhammad Zikri Adam", "F5512530117"),
    ("Trista Sheryl Lambei", "F5512530106")
]

courses_names = [
    "Learn JavaScript Fundamentals",
    "Learn Intermediate JavaScript",
    "Learn JavaScript Best Practices",
    "Learn Node.js",
    "Learn MongoDB"
]

for nama, nim in anggota_list:
    add_heading_2(f"8.{anggota_list.index((nama, nim)) + 1} Bukti Penyelesaian Course: {nama} ({nim})")
    for c in courses_names:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.4)
        r = p_c.add_run(f"• Bukti Course: {c}\n  [Lampiran Tangkapan Layar: Memperlihatkan Nama Lengkap Asli \"{nama}\" & Status Completed 100%]\n")
        r.font.italic = True
        r.font.size = Pt(10)

doc_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API.docx'
doc.save(doc_path)
print("Dokumen berhasil disimpan di:", doc_path)

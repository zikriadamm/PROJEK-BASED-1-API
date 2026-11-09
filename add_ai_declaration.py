import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API.docx'
out_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API_Lengkap.docx'
doc = docx.Document(doc_path)

# Tambahkan Page Break sebelum Halaman Deklarasi AI
doc.add_page_break()

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

# Judul Halaman Deklarasi
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(12)
p_title.paragraph_format.space_after = Pt(4)
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_title.add_run('HALAMAN DEKLARASI PENGGUNAAN GENERATIVE AI')
r.font.name = 'Times New Roman'
r.font.size = Pt(14)
r.font.bold = True

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_after = Pt(14)
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run('Evaluasi Sub-CPMK 4 — Project Based Learning (Rekayasa API)\nKelompok 2')
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(12)
r_sub.font.bold = True

# Pengantar
p_intro = doc.add_paragraph()
p_intro.paragraph_format.space_after = Pt(8)
p_intro.paragraph_format.line_spacing = 1.5
r_intro = p_intro.add_run(
    'Sesuai dengan ketentuan Etika dan Batasan Penggunaan Generative AI pada panduan tugas Evaluasi Sub-CPMK 4, '
    'kami yang bertanda tangan di bawah ini menyatakan secara jujur, transparan, dan bertanggung jawab mengenai '
    'penggunaan perangkat Generative Artificial Intelligence (AI) selama pengerjaan proyek ini. '
    'Deklarasi ini kami susun dengan rincian alat dan tujuan penggunaannya sebagai berikut:'
)
r_intro.font.name = 'Times New Roman'
r_intro.font.size = Pt(12)

# Tabel Deklarasi AI
table_ai = doc.add_table(rows=1, cols=4)
table_ai.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_ai.rows[0].cells
headers = ['No', 'Alat Generative AI', 'Keperluan & Bentuk Penggunaan', 'Langkah Verifikasi Mandiri']
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], 'E0E0E0')
    format_cell_borders(hdr_cells[i], top=True, bottom=True)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.bold = True
            r.font.size = Pt(10)

ai_data = [
    (
        '1',
        'Google Gemini / Antigravity AI Assistant',
        'Pemahaman Konsep & Diskusi Logika:\n• Mempelajari cara kerja event stream Node.js native (req.on("data") dan req.on("end")) untuk membaca body request.\n• Memahami formula matematika konversi kurs silang multi-valas terhadap acuan USD dan IDR.',
        'Memverifikasi langsung konsep melalui materi online course Codecademy (Learn Node.js & Learn Intermediate JavaScript) serta dokumentasi resmi nodejs.org.'
    ),
    (
        '2',
        'Google Gemini / Antigravity AI Assistant',
        'Penelusuran Penyebab Error (Debugging):\n• Menganalisis penyebab port terkunci (EADDRINUSE:3000) saat server di-restart.\n• Menelusuri penanganan asynchronous Promise rejection agar program client console tidak menampilkan stack trace saat skenario gagal.',
        'Melakukan uji coba mandiri baris demi baris, menambahkan penanganan try...catch terstruktur, dan menguji langsung menggunakan aplikasi Bruno.'
    ),
    (
        '3',
        'Google Gemini / Antigravity AI Assistant',
        'Peningkatan Keterbacaan Kode (Refactoring):\n• Membantu memisahkan fungsi helper modular (kirimJSON, kirimError, validasiPayload) agar sesuai kaidah Clean Code dan prinsip DRY (Don\'t Repeat Yourself).',
        'Meninjau ulang struktur kode, memastikan setiap anggota memahami fungsi setiap helper, dan menyesuaikan aturan validasi sesuai kebutuhan resource expenses kelompok.'
    ),
    (
        '4',
        'Google Gemini / Antigravity AI Assistant',
        'Perapian Format & Sistematika Laporan:\n• Membantu menyusun draf tabel pengujian dan sistematika 8 bab laporan sesuai ketentuan format panduan tugas.',
        'Seluruh teks laporan dibaca ulang dan disesuaikan dengan fakta implementasi teknis nyata yang dijalankan oleh kelompok.'
    )
]

for row in ai_data:
    r_cells = table_ai.add_row().cells
    for i, val in enumerate(row):
        r_cells[i].text = val
        format_cell_borders(r_cells[i], top=False, bottom=True)
        for p in r_cells[i].paragraphs:
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9)

# Pernyataan Tanggung Jawab
p_commit = doc.add_paragraph()
p_commit.paragraph_format.space_before = Pt(12)
p_commit.paragraph_format.space_after = Pt(8)
p_commit.paragraph_format.line_spacing = 1.5
r_commit = p_commit.add_run(
    'Pernyataan Integritas dan Penguasaan Materi:\n'
    '1. Kami menegaskan bahwa penulisan kode program TIDAK diserahkan secara buta kepada AI. Kode yang digunakan telah dipelajari, diuji, dan dipahami alur logikanya oleh setiap anggota tim sesuai pembagian tugas.\n'
    '2. Setiap anggota kelompok bertanggung jawab penuh atas bagian kode yang tercatat atas namanya, dan menyatakan SIAP SEDIA untuk menjelaskan logika program, menelusuri alur data dari request hingga response, maupun memodifikasi kode secara langsung pada sesi tanya jawab saat demo berlangsung di kelas.'
)
r_commit.font.name = 'Times New Roman'
r_commit.font.size = Pt(11)

# Tanda Tangan Anggota
p_ttd_loc = doc.add_paragraph()
p_ttd_loc.paragraph_format.space_before = Pt(8)
p_ttd_loc.paragraph_format.space_after = Pt(4)
p_ttd_loc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_ttd_loc = p_ttd_loc.add_run('Palu, Oktober 2026\nMenyatakan dengan sesungguhnya,')
r_ttd_loc.font.name = 'Times New Roman'
r_ttd_loc.font.size = Pt(11)

table_ttd = doc.add_table(rows=2, cols=4)
table_ttd.alignment = WD_TABLE_ALIGNMENT.CENTER

anggota_ttd = [
    ('Lidiya', 'F5512530118'),
    ('Tabita Creaselia B. T.', 'F5512520086'),
    ('Muhammad Zikri Adam', 'F5512530117'),
    ('Trista Sheryl Lambei', 'F5512530106')
]

for col_idx, (nama, nim) in enumerate(anggota_ttd):
    cell_top = table_ttd.cell(0, col_idx)
    cell_bot = table_ttd.cell(1, col_idx)
    
    cell_top.text = '\n\n\n(Tanda Tangan)'
    for p in cell_top.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.italic = True
            r.font.size = Pt(9)
            
    cell_bot.text = f'{nama}\nNIM. {nim}'
    for p in cell_bot.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.bold = True
            r.font.size = Pt(9.5)

doc.save(out_path)
print('Sukses menambahkan halaman Deklarasi AI ke dokumen Word:', out_path)

import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API_Lengkap.docx'
out_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API_Final.docx'
doc = docx.Document(doc_path)

# Table 4 is the AI table. Let's remove it from the document XML
t4 = doc.tables[4]
t4._element.getparent().remove(t4._element)

# Now let's find paragraph P827 (or the intro paragraph before the points)
# We can find the paragraph with text 'Deklarasi ini kami susun'
target_idx = None
for i, p in enumerate(doc.paragraphs):
    if 'Deklarasi ini kami susun' in p.text:
        target_idx = i
        break

print('Found target paragraph at index:', target_idx)

# Let's update P827 and insert the points right after it
doc.paragraphs[target_idx].text = (
    'Sesuai dengan pedoman Etika dan Batasan Penggunaan Generative AI pada panduan tugas Evaluasi Sub-CPMK 4, '
    'kami yang bertanda tangan di bawah ini menyatakan secara jujur, transparan, dan bertanggung jawab mengenai '
    'penggunaan perangkat Generative Artificial Intelligence (AI) selama pelaksanaan proyek ini. '
    'Rincian alat, keperluan, dan komitmen penguasaan materi kami susun dalam poin-poin berikut:'
)
for r in doc.paragraphs[target_idx].runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

# Next paragraph is currently P828 (Pernyataan integritas). Let's replace P828 with the complete structured points:
points_text = (
    '1. Alat Bantu Generative AI yang Digunakan:\n'
    '   Perangkat yang digunakan dalam proses diskusi adalah Google Gemini / Antigravity AI Assistant.\n\n'
    '2. Rincian Keperluan dan Bentuk Penggunaan:\n'
    '   a. Pemahaman Konsep dan Alur Logika:\n'
    '      Membantu memahami cara kerja event stream pada modul bawaan Node.js (req.on(\'data\') dan req.on(\'end\')) dalam membaca body request HTTP, serta formula matematika konversi kurs silang multi-valas terhadap acuan USD dan IDR.\n'
    '   b. Penelusuran Penyebab Error (Debugging):\n'
    '      Membantu menganalisis penyebab pesan kesalahan saat pengujian, seperti penanganan port yang terkunci (EADDRINUSE:3000), penanganan asynchronous Promise rejection, dan pencegahan munculnya pesan stack trace pada program client console saat skenario gagal.\n'
    '   c. Peningkatan Keterbacaan dan Struktur Kode (Refactoring):\n'
    '      Memberikan saran pemisahan fungsi-fungsi helper modular (kirimJSON, kirimError, dan validasiPayload) agar arsitektur kode lebih rapi, terstruktur, dan memenuhi prinsip Clean Code serta Don\'t Repeat Yourself (DRY).\n'
    '   d. Perapian Format dan Sistematika Laporan:\n'
    '      Membantu merapikan tata bahasa laporan, format tabel data, serta sistematika penulisan agar sesuai dengan rubrik penilaian tugas Sub-CPMK 4.\n\n'
    '3. Langkah Verifikasi dan Validasi Mandiri:\n'
    '   • Seluruh saran dan penjelasan teknis dari AI selalu diverifikasi kembali melalui materi kursus resmi Codecademy (Learn Node.js dan Learn Intermediate JavaScript) serta dokumentasi resmi Node.js (nodejs.org/docs).\n'
    '   • Kode program diuji secara langsung baris demi baris menggunakan terminal dan aplikasi Bruno untuk memastikan fungsionalitasnya berjalan nyata di lingkungan lokal kelompok.\n\n'
    '4. Pernyataan Integritas dan Penguasaan Materi:\n'
    '   • Kami menegaskan bahwa penulisan kode program tidak diserahkan secara buta kepada AI. Seluruh kode yang digunakan telah dipelajari, diuji, dan dipahami alur logikanya oleh setiap anggota tim sesuai dengan pembagian tugas.\n'
    '   • Setiap anggota kelompok bertanggung jawab penuh atas bagian kode yang tercatat atas namanya, dan menyatakan siap sedia untuk menjelaskan logika program, menelusuri alur data dari request hingga response, maupun memodifikasi kode secara langsung saat sesi tanya jawab demo di kelas.'
)

doc.paragraphs[target_idx + 1].text = points_text
for r in doc.paragraphs[target_idx + 1].runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
doc.paragraphs[target_idx + 1].paragraph_format.line_spacing = 1.3
doc.paragraphs[target_idx + 1].paragraph_format.space_after = Pt(10)

doc.save(out_path)
print('Sukses mengubah halaman Deklarasi AI menjadi bentuk per-poin di:', out_path)

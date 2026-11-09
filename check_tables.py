import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc_path = r'd:\Tugas semester 3\API\PROJEK BASED 1 API\Laporan_Proyek_PBL1_Rekayasa_API_Lengkap.docx'
doc = docx.Document(doc_path)

# Let's inspect paragraphs and tables at the end of the document
print("Total paragraphs:", len(doc.paragraphs))
print("Total tables:", len(doc.tables))

# The last table is the signature table (table index -1), and the second-to-last is the AI table (table index -2)
# Let's remove the AI declaration table and replace it with structured points!

# Let's see the tables
for i, t in enumerate(doc.tables):
    first_cell = t.cell(0, 0).text[:30]
    print(f"Table {i}: {first_cell}")

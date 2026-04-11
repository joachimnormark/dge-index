# Changelog - Version 2.2

## 🎉 v2.2 - PDF Fix + Forbedrede Downloads (Latest)

### 🔧 Fixed:
**PDF generering virker nu på Streamlit Cloud**
- Fjernet Kaleido dependency (krævede Chrome)
- Ny løsning: HTML + Excel downloads i stedet for PDF

### ✨ Nye download-muligheder:

**1. Download grafer som HTML (ZIP)**
- 7 interaktive HTML-filer
- Virker i alle browsere
- Inkluderer zoom, hover, og andre interaktive features
- Fil: `DGE_Grafer_YYYY.zip`

**2. Download data som Excel**
- Alle data fra de 7 tabeller
- Separate ark for hver tabel
- Nemt at arbejde videre med i Excel
- Fil: `DGE_Data_YYYY.xlsx`

### 📦 Dependencies opdateret:
**Fjernet (ikke længere nødvendige):**
- ❌ `reportlab` - PDF generation
- ❌ `Pillow` - Image processing
- ❌ `kaleido` - Chart to image (krævede Chrome)

**Kun nødvendige dependencies nu:**
- ✅ `streamlit` - Web framework
- ✅ `pandas` - Data manipulation
- ✅ `plotly` - Interactive charts
- ✅ `openpyxl` - Excel export
- ✅ `python-dateutil` - Date parsing

### 💡 Hvorfor denne ændring?

**Problem:**
PDF generering krævede Kaleido + Chrome, som ikke er installeret på Streamlit Cloud.

**Løsning:**
- HTML filer er interaktive og virker overalt
- Excel giver bedre adgang til rå data
- Simplere deployment (færre dependencies)

### 🎯 Hvad kan brugerne nu?

**HTML grafer (ZIP):**
- Download alle grafer som interaktive HTML
- Åbn i enhver browser
- Zoom, pan, hover for detaljer
- Del med kolleger (bare send ZIP)

**Excel data:**
- Alle tal fra analyserne
- Lav egne grafer og analyser
- Kombiner med andre data
- Import til andre systemer

---

## v2.1 - Nye tabeller

### Features:
- Tabel 6: Aktive grupper uden møder
- Tabel 7: SGE-modul grupper

---

## v2.0 - Major Update

### Features:
- 4-region mode
- Tabel 2 split (SUP vs DGE+JUN)
- Nye farver
- PDF download (depreceret i v2.2)

---

## v1.1 - Bug fixes
- KeyError fix

---

## v1.0 - Initial release
- Første version

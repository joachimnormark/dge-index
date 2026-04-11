# DGE Regional Sammenligning v2.2

Streamlit app til sammenligning af DGE mødeaktivitet på tværs af danske regioner.

## 🆕 Nyt i v2.2

- ✅ **Fixed**: PDF download virker nu (ingen Kaleido/Chrome krav)
- ✅ **Download grafer**: 7 interaktive HTML-filer i ZIP
- ✅ **Download data**: Alle tal som Excel fil
- ✅ **Simplere deployment**: Færre dependencies

## Sådan downloader du

### 📊 Grafer (HTML-format)
1. Klik "Download grafer"
2. Modtag ZIP-fil med 7 HTML-filer
3. Udpak og åbn i browser
4. Interaktive grafer med zoom, hover, osv.

### 📊 Data (Excel-format)
1. Klik "Download data"
2. Modtag Excel-fil med 8 ark
3. Åbn i Excel/Google Sheets
4. Lav dine egne analyser

## Features

### 📊 Tabel 1: Godkendte møder (indexeret)
- Stacked bar: DGE (🔵) / SUP (🔴) / JUN (🟢)
- Indbygger-justeret index (Midt = 100)

### 📊 Tabel 2A: Gruppestørrelse SUP (%)
- 100% stacked bar - kun SUP-grupper
- Kategorier: 🔴 0-4 | 🟠 5-7 | 🟡 8-10 | 🟢 11-13 | ⚪ 14+

### 📊 Tabel 2B: Gruppestørrelse DGE+JUN (%)
- 100% stacked bar - kun DGE og JUN-grupper
- Kategorier: 🔴 0-4 | 🟠 5-7 | 🟡 8-10 | 🟢 11-13 | ⚪ 14+

### 📊 Tabel 3: Deltagere pr. møde - SUP (%)
- 100% stacked bar
- Kategorier: 🔴 0-2 | 🟠 3-5 | 🟡 6-8 | 🟢 9-11 | ⚪ 12+

### 📊 Tabel 4: Deltagere pr. møde - DGE+JUN (%)
- 100% stacked bar
- Kategorier: 🔴 0-4 | 🟠 5-7 | 🟡 8-10 | 🟢 11-13 | ⚪ 14+

### 📊 Tabel 5: Møder pr. gruppe (%)
- 100% stacked bar - alle grupper
- Kategorier: 🔴 1-2 | 🟠 3-4 | 🟡 5-6 | 🟢 7-8 | ⚪ 9+

### 📊 Tabel 6: Aktive grupper uden godkendte møder
- Stacked bar: DGE (🔵) / SUP (🔴) / JUN (🟢)
- Absolutte tal (ikke indexeret)

### 📋 Tabel 7: Grupper med kun SGE-modul møder
- Datatabel med Region | Gruppenavn | Antal møder
- Sorteret efter region

## Installation

### Streamlit Cloud
```bash
# 1. Upload til GitHub:
#    - app.py
#    - requirements.txt

# 2. Deploy på share.streamlit.io
```

### Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Brug

1. **Vælg mode**: 4 eller 5 regioner
2. **Upload filer**: 8 eller 10 Excel-filer
3. **Vælg år**: 2020-2025
4. **Se analyser**: 7 tabeller
5. **Download**:
   - Grafer som HTML (ZIP)
   - Data som Excel

## Indbyggertal

| Region | Indbyggere | Note |
|--------|------------|------|
| Nord | 600.000 | - |
| **Midt** | **1.350.000** | **Base (index 100)** |
| Syd | 1.250.000 | - |
| Hovedstaden | 1.900.000 | 5-region mode |
| Sjælland | 850.000 | 5-region mode |
| Øst | 2.750.000 | 4-region mode |

## Data krav

### Groups file:
- Region, Gruppe ID, Gruppenavn
- Gruppetyper, Antal medlemmer, Status

### Meetings file:
- Region, Gruppe ID, Starttidspunkt
- Status, Antal deltagere, Mødetype

## Teknisk

**Dependencies:**
```
streamlit>=1.32.0
pandas>=2.2.1
numpy>=1.26.0
plotly>=5.19.0
openpyxl>=3.1.2
python-dateutil>=2.8.2
```

**Python:** 3.9+

Se [DATAFORMAT.md](DATAFORMAT.md) for detaljeret guide.

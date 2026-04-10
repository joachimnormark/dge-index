# DGE Regional Sammenligning v2.0

Streamlit app til sammenligning af DGE mødeaktivitet på tværs af danske regioner.

## 🆕 Nyt i v2.0

- ✅ Support for både 4 og 5 regioner
- ✅ Tabel 2 splittet i SUP vs DGE+JUN
- ✅ Nye farver i Tabel 1 (blå/rød/grøn)
- ✅ PDF download med alle grafer
- ✅ Forbedrede forklaringer

## Installation

### Option 1: Streamlit Cloud (anbefalet)
1. Opret GitHub repository
2. Upload `app.py` og `requirements.txt`
3. Gå til [share.streamlit.io](https://share.streamlit.io)
4. Klik "New app"
5. Vælg dit repo og `app.py`
6. Deploy!

### Option 2: Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Brug

### 1. Vælg mode
- **5 regioner**: Upload 10 filer (Nord, Midt, Syd, Hovedstaden, Sjælland)
- **4 regioner**: Upload 8 filer (Nord, Midt, Syd, Øst)

### 2. Upload filer
**5-region mode (10 filer):**
- 2 filer for Nord (groups + meetings)
- 2 filer for Midt (groups + meetings)
- 2 filer for Syd (groups + meetings)
- 2 filer for Hovedstaden (groups + meetings)
- 2 filer for Sjælland (groups + meetings)

**4-region mode (8 filer):**
- 2 filer for Nord (groups + meetings)
- 2 filer for Midt (groups + meetings)
- 2 filer for Syd (groups + meetings)
- 2 filer for Øst (groups + meetings)

### 3. Vælg år
Vælg hvilket år der skal analyseres (2020-2025)

### 4. Se analyser
6 tabeller genereres automatisk

### 5. Download PDF
Klik "Download som PDF" for at få alle grafer som PDF

## Indbyggertal

| Region | Indbyggere | Index base |
|--------|------------|------------|
| Nord (Nordjylland) | 600.000 | - |
| **Midt (Midtjylland)** | **1.350.000** | **100** |
| Syd (Syddanmark) | 1.250.000 | - |
| Hovedstaden | 1.900.000 | - |
| Sjælland | 850.000 | - |
| Øst (Hovedstaden + Sjælland) | 2.750.000 | - |

## Tabeller

### 📊 Tabel 1: Godkendte møder (indexeret)
- Stacked bar: DGE (🔵) / SUP (🔴) / JUN (🟢)
- Indbygger-justeret index (Midt = 100)
- Viser detaljerede tal i expander

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

## Data krav

Se [DATAFORMAT.md](DATAFORMAT.md) for detaljeret guide

### Groups file (påkrævet kolonner):
- Region
- Gruppe ID
- Gruppenavn
- Gruppetyper (DGE/Supervision/Junior)
- Antal medlemmer

### Meetings file (påkrævet kolonner):
- Region
- Gruppe ID
- Starttidspunkt
- Status (skal være "Godkendt" for at tælle)
- Antal deltagere

## Region mapping

| Excel fil indeholder | Mappes til |
|---------------------|------------|
| "Region Nordjylland" | Nord |
| "Region Midtjylland" | Midt |
| "Region Syddanmark" | Syd |
| "Region Hovedstaden" | Hovedstaden |
| "Region Sjælland" | Sjælland |
| "Region Øst" | Øst |

## Teknisk stack

- **Python 3.9+**
- **Streamlit** - Web interface
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **ReportLab** - PDF generation
- **Kaleido** - Chart to image export

## Support

Ved problemer:
1. Tjek [DATAFORMAT.md](DATAFORMAT.md)
2. Verificer fil-kolonner
3. Tjek region-navne
4. Se [CHANGELOG_v2.md](CHANGELOG_v2.md) for ændringer

## Licens

Udviklet til DGE regional analyse

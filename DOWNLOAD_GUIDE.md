# Download Guide

## 📥 To download-muligheder

Appen tilbyder nu **to** måder at downloade dine analyser:

1. **Grafer som HTML** (interaktive)
2. **Data som Excel** (til videre analyse)

---

## 📊 Download grafer (HTML)

### Hvad får du?
En ZIP-fil med **7 interaktive HTML-filer**:
- `tabel_1_moeder.html`
- `tabel_2a_sup.html`
- `tabel_2b_dge_jun.html`
- `tabel_3_deltagere_sup.html`
- `tabel_4_deltagere_dge_jun.html`
- `tabel_5_moeder_pr_gruppe.html`
- `tabel_6_uden_moeder.html`

### Hvordan bruger du dem?

**1. Download ZIP**
- Klik "Download grafer"
- Gem ZIP-filen

**2. Udpak**
```bash
# Windows: Højreklik → "Udpak alle"
# Mac: Dobbeltklik ZIP-filen
# Linux: unzip DGE_Grafer_2025.zip
```

**3. Åbn HTML-filer**
- Dobbeltklik på en .html fil
- Åbnes i din standard browser
- **Ingen internet krævet** (efter første åbning)

### Hvad kan du gøre?

**Interaktive features:**
- 🔍 **Zoom**: Træk for at zoome ind på område
- 🖱️ **Hover**: Hold musen over for detaljer
- 👁️ **Toggle**: Klik legend for at skjule/vise serier
- 💾 **Gem**: Download graf som PNG (klik kamera-ikon)

**Brug cases:**
- Del med kolleger (send bare HTML-filen)
- Præsentation (åbn i browser på møde)
- Print (fra browser: Ctrl+P)
- Arkivering (gem for fremtidig reference)

---

## 📊 Download data (Excel)

### Hvad får du?
En Excel-fil med **8 ark**:
- `T1-Møder` - Godkendte møder (indexeret)
- `T2A-SUP` - Gruppestørrelse SUP
- `T2B-DGE+JUN` - Gruppestørrelse DGE+JUN
- `T3-Deltagere SUP` - Deltagere pr. møde (SUP)
- `T4-Deltagere DGE+JUN` - Deltagere pr. møde (DGE+JUN)
- `T5-Møder pr gruppe` - Mødefrekvens
- `T6-Uden møder` - Aktive grupper uden møder
- `T7-SGE-modul` - Grupper med kun SGE-møder

### Hvordan bruger du dem?

**1. Download Excel**
- Klik "Download data"
- Gem .xlsx-filen

**2. Åbn i Excel/Google Sheets**
```bash
# Excel: Dobbeltklik filen
# Google Sheets: Upload til Google Drive
# LibreOffice: Åbn med Calc
```

### Hvad kan du gøre?

**Analyse:**
- Lav dine egne grafer
- Beregn ekstra statistik
- Kombiner med andre data
- Pivot tables for dybere indsigt

**Rapportering:**
- Kopiér tal til Word/PowerPoint
- Eksportér til andre formater
- Del specifik data med teams

**Integration:**
- Importér til BI-systemer
- Automatiser videre processing
- Arkivér i databaser

---

## 🆚 HTML vs Excel - Hvornår bruger du hvad?

### Brug HTML når du vil:
✅ Vise grafer til andre
✅ Præsentere på møder
✅ Have interaktive visualiseringer
✅ Hurtigt dele resultater
✅ Arkivere visuelle rapporter

### Brug Excel når du vil:
✅ Lave dine egne analyser
✅ Kombinere med andre data
✅ Lave custom grafer
✅ Dele rå tal
✅ Importere til andre systemer

### Tip: Download begge! 💡
De komplementerer hinanden:
- HTML til præsentation
- Excel til analyse

---

## ❓ FAQ

### Q: Kan jeg åbne HTML-filer uden internet?
**A:** Ja! Efter første åbning loades Plotly biblioteket, og derefter virker alt offline.

### Q: Virker HTML-filerne på alle enheder?
**A:** Ja! Fungerer i alle moderne browsere (Chrome, Firefox, Safari, Edge).

### Q: Kan jeg redigere graferne i HTML?
**A:** Nej, men du kan:
- Zoome og interagere
- Downloade som PNG
- Kopiér data til clipboard
For redigering: Brug Excel-dataene til at lave dine egne grafer

### Q: Hvorfor ikke PDF?
**A:** HTML er bedre fordi:
- ✅ Interaktive features
- ✅ Bedre kvalitet
- ✅ Virker på alle platforme
- ✅ Ingen ekstra software nødvendig
- ✅ Mindre filstørrelse

### Q: Kan jeg få PDF alligevel?
**A:** Ja, du kan:
1. Åbn HTML i browser
2. Print to PDF (Ctrl+P → Gem som PDF)
3. Eller: Åbn i Word og eksportér som PDF

---

## 💡 Pro tips

### For bedste oplevelse:

**HTML:**
```
1. Udpak alle filer til samme mappe
2. Åbn i Chrome/Firefox for bedste performance
3. Brug fuld skærm (F11) til præsentationer
4. Gem graferne som PNG for Word/PowerPoint
```

**Excel:**
```
1. Aktivér "Data Analysis ToolPak" i Excel
2. Brug Conditional Formatting til at fremhæve mønstre
3. Lav Pivot Tables for hurtig summering
4. Gem som .csv for import til andre systemer
```

### Automatisering:

Download samme type hver uge/måned:
```python
# Eksempel: Download data programmatisk
# (kræver Streamlit API access)
```

---

## 🛠️ Troubleshooting

### HTML ikke interaktiv?
- Tjek at JavaScript er aktiveret i browser
- Prøv anden browser
- Tøm browser cache

### Excel ser mærkelig ud?
- Tjek at du bruger Excel 2016+ eller Google Sheets
- Prøv at åbne med LibreOffice Calc
- Kontakt support hvis kolonner mangler

### ZIP-fil kan ikke åbnes?
- Sørg for filen er fuldt downloaded
- Tjek at filstørrelsen matcher (> 1 MB)
- Prøv anden zip-program (7-Zip, WinRAR)

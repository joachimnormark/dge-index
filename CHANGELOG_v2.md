# Changelog - Version 2.0

## 🎉 v2.0 - Major Update (Latest)

### ✨ Nye features:

**1. Support for 4-region mode**
- Kan nu håndtere 8 filer (4 regioner) ELLER 10 filer (5 regioner)
- Ny region: "Øst" (kombineret Hovedstaden + Sjælland)
- Indbyggertal Øst: 2.750.000
- Vælger ved upload: 4 eller 5 regioner

**2. Tabel 2 splittet i 2A og 2B**
- **Tabel 2A**: Gruppestørrelse - kun SUP-grupper
- **Tabel 2B**: Gruppestørrelse - kun DGE og JUN-grupper
- Samme procent-visualisering for begge

**3. Opdaterede farver i Tabel 1**
- 🔵 DGE = Blå (#2B6CB0)
- 🔴 SUP = Rød (#DC2626)
- 🟢 JUN = Grøn (#10B981)

**4. Farveforklaringer**
- **Tabel 1**: Rækkefølge DGE, SUP, JUN
- **Alle andre tabeller**: Laveste først (rød → orange → gul → grøn → grå)
- Forklaringer matcher grafer

**5. PDF Download**
- Download knap nederst på siden
- Genererer PDF med alle 6 grafer
- Landscape format (A4)
- Titel med årstal
- Automatisk filnavn: `DGE_Regional_Sammenligning_YYYY.pdf`

### 🔧 Tekniske ændringer:

**Dependencies tilføjet:**
- `reportlab>=4.0.0` - PDF generering
- `Pillow>=10.0.0` - Billedbehandling  
- `kaleido>=0.2.1` - Plotly til billede-eksport

**Nye konstanter:**
```python
REGION_ORDER_5 = ['Nord', 'Midt', 'Syd', 'Hovedstaden', 'Sjælland']
REGION_ORDER_4 = ['Nord', 'Midt', 'Syd', 'Øst']
GROUP_TYPE_COLORS = {'DGE': '#2B6CB0', 'SUP': '#DC2626', 'JUN': '#10B981'}
```

**Nye funktioner:**
- `generate_pdf_with_charts()` - PDF generering med grafer

### 📊 Tabeller nu:

1. **Tabel 1**: Godkendte møder (indexeret) - med nye farver
2. **Tabel 2A**: Gruppestørrelse SUP (%) 
3. **Tabel 2B**: Gruppestørrelse DGE+JUN (%)
4. **Tabel 3**: Deltagere SUP (%)
5. **Tabel 4**: Deltagere DGE+JUN (%)
6. **Tabel 5**: Møder pr. gruppe (%)

---

## v1.1 - Bug fixes

### Fixed:
- KeyError i Tabel 5 (Gruppe ID manglede)
- Gruppetype merge flyttet til før alle tabeller

---

## v1.0 - Initial release

### Features:
- 5 tabeller med regional sammenligning
- Indexerede tal (Midt = 100)
- Procentfordelinger
- Support for 10 filer

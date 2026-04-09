# DGE Regional Sammenligning

Streamlit app til sammenligning af DGE mødeaktivitet på tværs af 5 danske regioner.

## Installation

1. Opret GitHub repository
2. Upload `app.py` og `requirements.txt`
3. Deploy på Streamlit Cloud
4. Peg på `app.py` som entry point

## Datafiler

Appen kræver **10 Excel-filer** (2 per region):

### Region mapping:
- **Nord** (Nordjylland): ~600.000 indbyggere
- **Midt** (Midtjylland): ~1.350.000 indbyggere ← Base for index
- **Syd** (Syddanmark): ~1.250.000 indbyggere
- **Hovedstaden**: ~1.900.000 indbyggere
- **Sjælland**: ~850.000 indbyggere

### Påkrævede filer per region:
1. `workspace_groups_all-XX.xlsx` - Gruppedata
2. `workspace_meetings_all-XX.xlsx` - Mødedata

### Påkrævede kolonner:

**Groups file:**
- Region
- Gruppe ID
- Gruppenavn
- Gruppetyper (DGE, Supervision, Junior)
- Antal medlemmer

**Meetings file:**
- Region
- Gruppe ID
- Starttidspunkt
- Status
- Antal deltagere

## Features

### Tabel 1: Antal godkendte møder (indexeret)
- Stacked bar chart med DGE/SUP/JUN
- Indbygger-justeret index (Midt = 100)
- Detaljerede tal i expander

### Tabel 2: Gruppestørrelse (%)
- 100% stacked bar
- Kategorier: 0-4, 5-7, 8-10, 11-13, 14+
- Farver: Rød → Orange → Gul → Grøn → Grå

### Tabel 3: Deltagere pr. møde (SUP-grupper, %)
- 100% stacked bar
- Kategorier: 0-2, 3-5, 6-8, 9-11, 12+
- Farver: Rød → Orange → Gul → Grøn → Grå

### Tabel 4: Deltagere pr. møde (DGE+JUN grupper, %)
- 100% stacked bar
- Kategorier: 0-4, 5-7, 8-10, 11-13, 14+
- Farver: Rød → Orange → Gul → Grøn → Grå

### Tabel 5: Møder pr. gruppe (%)
- 100% stacked bar
- Kategorier: 1-2, 3-4, 5-6, 7-8, 9+
- Farver: Rød → Orange → Gul → Grøn → Grå

## Brug

1. Upload 10 Excel-filer
2. Vælg år
3. Se visualiseringer

## Teknisk

- Python 3.9+
- Streamlit
- Pandas for databehandling
- Plotly for visualisering

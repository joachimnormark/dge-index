# Changelog

## v1.1 - Bug fixes (Latest)

### Fixed:
- **KeyError i Tabel 5**: Fixed missing 'Gruppe ID' column error
  - Moved gruppetype merge to before all tables
  - Added fallback til Gruppenavn hvis Gruppe ID ikke findes
  - Tabel 5 bruger nu korrekt dataframe (meetings_with_type)
  
### Changes:
- Merge af groups og meetings data sker nu én gang før alle tabeller
- Automatisk fallback fra Gruppe ID til Gruppenavn hvis nødvendigt
- Bedre error handling ved manglende kolonner

## v1.0 - Initial release

### Features:
- Tabel 1: Indexerede mødeantal (Midt = 100)
- Tabel 2: Gruppestørrelse fordeling (%)
- Tabel 3: Deltagere pr. møde - SUP (%)
- Tabel 4: Deltagere pr. møde - DGE+JUN (%)
- Tabel 5: Møder pr. gruppe (%)
- Support for 10 filer (2 per region)
- Automatisk region-mapping

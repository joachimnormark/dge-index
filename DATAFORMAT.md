# Data Format Guide

## Fil-navngivning

Upload præcis **10 filer** til appen:

```
workspace_groups_all-11.xlsx    (Nord)
workspace_meetings_all-9.xlsx   (Nord)

workspace_groups_all-13.xlsx    (Midt)
workspace_meetings_all-11.xlsx  (Midt)

workspace_groups_all-14.xlsx    (Syd)
workspace_meetings_all-12.xlsx  (Syd)

workspace_groups_all-12.xlsx    (Hovedstaden)
workspace_meetings_all-10.xlsx  (Hovedstaden)

workspace_groups_all-15.xlsx    (Sjælland)
workspace_meetings_all-13.xlsx  (Sjælland)
```

## Region-mapping

Hver fil skal have en **Region** kolonne med ét af disse navne:

- `Region Nordjylland` → Nord
- `Region Midtjylland` → Midt
- `Region Syddanmark` → Syd
- `Region Hovedstaden` → Hovedstaden
- `Region Sjælland` eller `Region Sjælland , KAP-S` → Sjælland

## Groups file struktur

Påkrævede kolonner:
```
Region              | Text    | "Region Nordjylland"
Gruppe ID           | Number  | 12345
Gruppenavn          | Text    | "12-mandsgruppe Nord"
Gruppetyper         | Text    | "DGE" eller "Supervision" eller "Junior"
Antal medlemmer     | Number  | 12
Status              | Text    | "Aktiv" eller "Inaktiv"
```

## Meetings file struktur

Påkrævede kolonner:
```
Region              | Text     | "Region Nordjylland"
Gruppe ID           | Number   | 12345
Gruppenavn          | Text     | "12-mandsgruppe Nord"
Starttidspunkt      | Datetime | "15. januar 2025, kl. 19:00"
Status              | Text     | "Godkendt"
Antal deltagere     | Number   | 10
Mødetype            | Text     | "DGE-møde"
```

## Gruppetype mapping

Appen mapper automatisk:
- Indeholder "DGE" → DGE
- Indeholder "SUPERVISION" eller "SUP" → SUP
- Indeholder "JUNIOR" eller "JUN" → JUN
- Alt andet → Andet (filtreres fra)

## Test data kvalitet

Før upload, tjek:
- [ ] Alle filer har Region kolonne
- [ ] Alle groups har Gruppe ID
- [ ] Alle meetings har Gruppe ID der matcher groups
- [ ] Datoer er i dansk format
- [ ] Status er enten "Godkendt", "Afvist" osv.
- [ ] Antal medlemmer og deltagere er tal (ikke tekst)

## Fejlfinding

Hvis appen fejler:
1. Tjek at præcis 10 filer er uploaded
2. Verificer kolonnenavne (case-sensitive)
3. Tjek Region-navne matcher ovenstående
4. Verificer Gruppe ID findes i begge filer
5. Tjek datoformat er dansk

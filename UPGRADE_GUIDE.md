# Upgrade Guide til v2.0

## 🎯 Hvad er nyt?

### 1. ⭐ 4-region eller 5-region mode
**Før:** Kun 5 regioner (10 filer)
**Nu:** Vælg mellem 4 eller 5 regioner

**Hvordan:**
- Vælg mode øverst: "5 regioner" eller "4 regioner"
- Upload 10 filer (5 regioner) ELLER 8 filer (4 regioner)
- I 4-region mode: Brug "Region Øst" i stedet for Hovedstaden+Sjælland

### 2. 📊 Tabel 2 splittet
**Før:** Én tabel med alle grupper
**Nu:** To tabeller
- **Tabel 2A**: Kun SUP-grupper
- **Tabel 2B**: Kun DGE+JUN-grupper

**Fordel:** Bedre sammenligning af forskellige gruppetyper

### 3. 🎨 Nye farver i Tabel 1
**Før:** Standard Plotly farver
**Nu:** DGE-specifikke farver
- 🔵 DGE = Blå
- 🔴 SUP = Rød  
- 🟢 JUN = Grøn

### 4. 📋 Farveforklaringer opdateret
**Før:** Ikke konsistent rækkefølge
**Nu:** 
- **Tabel 1**: DGE, SUP, JUN
- **Alle andre**: Rød → Orange → Gul → Grøn → Grå (laveste først)

### 5. 📄 PDF Download
**NYT!** Download alle 6 grafer som PDF
- Klik "Download som PDF" nederst
- Landscape format
- Professionel layout
- Filnavn: `DGE_Regional_Sammenligning_YYYY.pdf`

## 📦 Deployment ændringer

### requirements.txt opdateret
Tilføjet nye dependencies:
```
reportlab>=4.0.0
Pillow>=10.0.0
kaleido>=0.2.1
```

**Handling:** Upload ny `requirements.txt` til GitHub

## 🔄 Migration steps

### Hvis du kører på Streamlit Cloud:

1. **Backup nuværende version** (optional)
   ```
   git tag v1.1
   git push --tags
   ```

2. **Upload nye filer**
   - Erstat `app.py` med ny version
   - Erstat `requirements.txt` med ny version

3. **Redeploy**
   - Streamlit Cloud auto-deployer ved git push
   - Eller klik "Reboot app" i dashboard

4. **Test**
   - Upload test-data
   - Verificer alle tabeller vises
   - Test PDF download

### Hvis du kører lokalt:

1. **Installer nye dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Genstart app**
   ```bash
   streamlit run app.py
   ```

## ⚠️ Breaking changes

**INGEN** - Alle eksisterende features virker stadig!

5-region mode fungerer præcis som før. Du kan fortsætte med 10 filer uden ændringer.

## 🐛 Kendte problemer

### PDF generation kan fejle hvis:
- Kaleido ikke er installeret korrekt
- Ikke nok hukommelse (store datasæt)

**Løsning:** Prøv at redeploy eller kontakt Streamlit support

## 💡 Tips

### Brug 4-region mode når:
- Data for Hovedstaden og Sjælland er kombineret
- Du vil simplificere sammenligning
- Færre datapunkter er tilstrækkelige

### Brug 5-region mode når:
- Du har separate data for hver region
- Detaljeret sammenligning ønskes
- Maksimal granularitet er vigtig

## 📞 Support

Problemer? Check:
1. [README.md](README.md) - Komplet guide
2. [DATAFORMAT.md](DATAFORMAT.md) - Data krav
3. [CHANGELOG_v2.md](CHANGELOG_v2.md) - Alle ændringer

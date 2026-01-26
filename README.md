# Koidulauliku E-laulik 🎵

ASI Karika 2026 koduvooru lahendus - veebirakendus Koidulauliku vaimule

## 📖 Kirjeldus

Koidulauliku E-laulik on veebirakendus, mis on loodud spetsiaalselt Koidulauliku vaimule, et aidata tal kergesti ja kiiresti tutvuda kaasaegse Eesti kultuurieluga. Rakendus kogub automaatselt infot mitmest usaldusväärsest allikast ja esitab selle arusaadaval ja kasutajasõbralikul kujul.

## ✨ Funktsionaalsus

- **📰 Uudised**: Värskemad uudised Eesti kultuurist ERR.ee ja Postimees.ee portaalidest
- **🎭 Sündmused**: Kultuuriüritused, kontserdid ja festivaalid Eesti kultuurisündmused portaalist
- **📚 Kultuuriinfo**: Põhjalik informatsioon Eesti kultuurist Wikipediast
- **🔍 Otsing**: Võimalus otsida infot kõigist kategooriatest
- **📱 Responsiivne**: Töötab nii arvutis kui mobiilseadmes

## 🌐 Andmeallikad

Rakendus kogub andmeid järgmistest allikatest:

1. **ERR Kultuur (kultuur.err.ee)** - Eesti Rahvusringhääling (kultuuriuudised ja artiklid)
2. **Postimees.ee** - Üks Eesti suurimaid uudisteportaale
3. **Kultuurikava (kultuurikava.ee/events/)** - Kultuuriürituste portaal
4. **Piletilevi (piletilevi.ee)** - Piletimüügi portaal (kultuuriüritused koos piltidega)
5. **Eesti kultuurisündmused** - Eesti kultuuriportaal (sündmused ja üritused)
6. **Wikipedia (et.wikipedia.org)** - Vaba entsüklopeedia (Eesti kultuuri artiklid)

## 🛠️ Teknoloogiad

- **Python 3.8+** - Programmeerimiskeel
- **Flask 3.0.0** - Veebirakenduse raamistik
- **BeautifulSoup4** - HTML-i ja XML-i parsimine
- **Scrapy 2.11.0** - Struktureeritud web scraping raamistik
- **Requests** - HTTP päringud
- **lxml** - XML/HTML töötlemine
- **HTML/CSS/JavaScript** - Kasutajaliides

## 🚀 Kiirstart

### Eeldused

- Python 3.8 või uuem
- pip (Python package installer)

### Installimine

1. Kloonige repositoorium:
```bash
git clone https://github.com/artjom3729/Koidulauliku-E-laulik.git
cd Koidulauliku-E-laulik
```

2. Looge virtuaalne keskkond (soovitatav):
```bash
python -m venv venv
source venv/bin/activate  # Linuxis/macOS
# VÕI
venv\Scripts\activate  # Windowsis
```

3. Installige sõltuvused:
```bash
pip install -r requirements.txt
```

### Käivitamine

```bash
python app.py
```

Avage brauser ja minge aadressile: `http://localhost:5000`

## 📁 Projekti struktuur

```
Koidulauliku-E-laulik/
│
├── app.py                     # Põhirakendus (Flask)
├── requirements.txt           # Python sõltuvused
├── juhend.txt                # Detailne juhend
├── README.md                 # See fail
├── AI_USAGE.txt              # AI kasutamise dokumentatsioon
│
├── scrapers/                 # Andmete kogumise moodulid
│   ├── __init__.py
│   ├── err_scraper.py           # ERR Kultuur uudiste scraper (BeautifulSoup)
│   ├── postimees_scraper.py     # Postimees.ee uudiste scraper
│   ├── culture_scraper.py       # Eesti kultuurisündmused sündmuste scraper
│   ├── kultuurikava_scraper.py  # Kultuurikava.ee sündmuste scraper
│   ├── piletilevi_scraper.py    # Piletilevi.ee sündmuste scraper (pildid)
│   ├── wikipedia_scraper.py     # Wikipedia kultuuriinfo scraper
│   ├── scrapy_settings.py       # Scrapy konfiguratsioon
│   ├── pipelines.py             # Scrapy andmete töötlemise pipeline
│   └── spiders/                 # Scrapy spider'id
│       ├── __init__.py
│       ├── err_spider.py        # ERR Kultuur Scrapy spider
│       ├── kultuurikava_spider.py  # Kultuurikava Scrapy spider
│       └── piletilevi_spider.py    # Piletilevi Scrapy spider
│
├── templates/                # HTML mallid
│   ├── base.html                # Baas mall
│   ├── index.html               # Avaleht
│   ├── uudised.html             # Uudiste leht
│   ├── syndmused.html           # Sündmuste leht
│   ├── kultuur.html             # Kultuuri leht
│   └── info.html                # Info leht
│
└── static/                   # Staatilised failid
    ├── css/
    │   └── style.css            # Stiilileht
    └── js/
        └── main.js              # JavaScript
```

## 📝 Kasutamine

1. **Avaleht**: Ülevaade kõigist kategooriatest ja otsing
2. **Uudised**: Klikake "Uudised" menüüs, et näha värskemaid uudiseid
3. **Sündmused**: Vaadake kultuuriüritusi ja nende detaile
4. **Kultuur**: Lugege Eesti kultuuri kohta Wikipediast
5. **Otsing**: Kasutage avalehe otsingukasti, et leida konkreetset infot

## 🎨 Autoriõigused ja litsentsid

### Kasutatud materjalid

- **Rakenduse kood**: Autori enda loodud
- **Google Fonts (Roboto)**: Apache License 2.0
- **Wikipedia sisu**: Creative Commons Attribution-ShareAlike 3.0 Unported License
- **ERR.ee, Postimees.ee, Eesti kultuurisündmused**: Avalikud allikad, kasutatud ainult viited

### Litsents

See projekt on loodud hariduslikel eesmärkidel ASI Karika 2026 koduvooru raames.

## 🤖 AI Kasutamine

AI (GitHub Copilot, ChatGPT) kasutamine on dokumenteeritud failis `AI_USAGE.txt`.

## 📞 Kontakt

Küsimuste või probleemide korral:
- Vaadake `juhend.txt` faili detailsete juhiste saamiseks
- Kontrollige, et kõik sõltuvused on installitud
- Veenduge, et Python versioon on 3.8 või uuem

## 🏆 ASI Karika 2026

See projekt on loodud ASI Karika koduvooru ülesande raames. Projekti eesmärk on luua kasutajasõbralik rakendus, mis aitab kiiresti leida ja avastada infot Eesti kultuuri kohta.

### Hindamiskriteeriumid

- ✅ **Informatsiooni rohkus**: 6 erinevat allikat (ERR Kultuur, Postimees, Kultuurikava, Piletilevi, Eesti kultuurisündmused, Wikipedia)
- ✅ **Web scraping tehnoloogiad**: BeautifulSoup ja Scrapy kasutamine
- ✅ **Pildid kultuuriüritustest**: Piltide kogumine Piletilevi ja teistest allikatest
- ✅ **Informatsiooni õigsus**: Usaldusväärsed allikad, automaatne andmete kogumine
- ✅ **Kasutajakogemus**: Lihtne ja loogiline kasutada, selge navigatsioon
- ✅ **Loomingulisus**: Responsiivne disain, otsingu funktsioon, fallback andmed

---

**Loodud ❤️-ga ASI Karika 2026 koduvooru jaoks**

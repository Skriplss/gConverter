<div style="text-align: center;">
   <h1>gConvertor</h1>
  <h3>Konvertor G-kódu do formátu RAPID</h3>

[![Python 3.12.8](https://img.shields.io/badge/python-3.12.8-blue.svg)](https://www.python.org/downloads/release/python-3128/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-green.svg)](https://github.com/yourusername/gconvertor)
</div>

##  Popis

Nástroj na konverziu G-kódu robotickej 3D tlačiarne do formátu rapid. Tento nástroj založený na Pythone poskytuje grafické rozhranie na konverziu súborov G-kódu do formátu rapid pre robotické systémy.

##  Funkcie

-  Grafické používateľské rozhranie pre jednoduchú konverziu súborov
-  Podpora pre parsovanie a transformáciu G-kódu
-  Možnosti vizualizácie konvertovaných súborov
-  Generovanie výstupu vo formáte rapid
-  Spracovanie vstupných a výstupných súborov
-  Spracovanie založené na workeri pre lepší výkon

##  Technológie

- ![Python](https://img.shields.io/badge/Python-3.12.8-3776AB?style=flat&logo=python&logoColor=white)
- ![wxPython](https://img.shields.io/badge/wxPython-GUI-lightgrey)
- Vlastný parser G-kódu
- Vizualizačné nástroje

##  Inštalácia

### Predpoklady
- Python 3.12.8
- pip (Python package manager)

### Kroky inštalácie

1. Klonovanie repozitára:
```bash
git clone [repository-url]
cd gconvertor
```

2. Inštalácia potrebných závislostí:
```bash
pip install -r requirements.txt
```

##  Použitie

1. Spustenie aplikácie:
```bash
python gconverter.py
```

2. Cez grafické rozhranie:
   -  Vyberte vstupný súbor G-kódu
   -  Nakonfigurujte parametre konverzie
   -  Vyberte umiestnenie výstupu
   -  Spustite konverziu

## Vývoj: linting a automatické formátovanie
- Ručné spustenie linera: `make lint`
- Ručné spustenie formatera: `make format`
- Na automatické formátovanie: `black . && isort .`


##  Licencia

[MIT]

##  Stav projektu

![Status](https://img.shields.io/badge/Status-In%20Development-green.svg)









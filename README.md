# 'Soveltava matematiikka ja fysiikka ohjelmoinnissa' kurssin fysiikan osuuden loppuprojekti
Virtuaaliympäristössä samat paketit kuin kurssilla, poislukien black formatter.

## Itselle muistiin miten saa nopeasti uuden venvin ja asenneltua paketit:
### Asenna uusi virtuaalinen ympäristö
```bash
py -m venv .venv
```
jupyter notebooks ei näyttäny hyväksyvän näin pika-asennuksena muuta kuin defaultin '.venv' projektin juureen.
Jos haluaa tehdä yleisen usealle projektille, piti tehdä se toisella tyylillä:
```bash
py -m ipykernel install --user --name=<venv_name> --display-name "Python (<venv_name>)"
```
### Aktivoi virtuaalinen ympäristo
Nämä on windowsilla. Linuxille taitaa olla hiukan erit komennot?
#### git bash
```bash
source ./venv/Scripts/activate
```
#### cmd
```cmd
.venv\Scripts\activate
```
### Asenna paketit tiedostosta
```bash
py -m pip install -r requirements.txt
```
Joskus git bash / cmd / vscoden terminaalit menee sekaisin. Turvallisempaa asennella ne 'py -m' prefixillä

## helperfunctions.py
Kootut apurifunktiot

## komponentit.ipynb
Testailua plotterilla
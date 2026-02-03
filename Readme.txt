# Conway's Game of Life

Implementacja gry „Game of Life” Johna Conwaya z możliwością edycji planszy przez użytkownika.

---

## Autorzy
- Igor Wawrzeńczak - 293164
- Damian Sobieraj - 293178

---

## Wymagania
- Python 3.10 lub nowszy
- pip

---

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/Igorson1/Conways-Game-Of-Life.git
cd ConwaysGameOfLife

2. Utwórz środowisko wirtualne
```bash
python -m venv .venv

3. Aktywuj środowisko
```bash
source .venv/bin/activate

4. Zainstaluj wymagane pakiety
```bash
pip install -r requirements.txt

5. Uruchamianie programu
```bash
python main.py

Program przyjmuje argumenty:
--szybkosc (szybkość symulacji (1-50). domyślnie: 4)
--rozmiar (rozmiar siatki (1-7) (liczba komórek w rzędzie/kolumnie). domyślnie: 1)
--przypadek (wybierz początkowy wzór)

Więcej informacji po wpisaniu:
```bash
python main.py -h


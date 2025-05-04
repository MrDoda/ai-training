# Úkol 5 - Věňovo dilema

#### Daniel Král

v tomto dokumentu předkládám výsledky analýzy vlivu různých metod selekce na výkon mého evolučního algoritmu v opakovaném vězňově dilematu.

## Klíčové poznatky

1. **Tournament (tournsize=3)**

   - Průměrné roky na kolo: 1,113
   - Nejlepší roky na kolo: 1,018

2. **Tournament (tournsize=5)**

   - Průměrné roky na kolo: 1,061
   - Nejlepší roky na kolo: 1,001

3. **Roulette**

   - Průměrné roky na kolo: 1,184
   - Nejlepší roky na kolo: 1,036

4. **Random**

   - Průměrné roky na kolo: 2,250
   - Nejlepší roky na kolo: 1,796

## Tabulka výsledků

| Metoda selekce   | Průměrné roky | Nejlepší roky |
| ---------------- | ------------: | ------------: |
| **tournament_3** |         1,113 |         1,018 |
| **tournament_5** |         1,061 |         1,001 |
| **roulette**     |         1,184 |         1,036 |
| **random**       |         2,250 |         1,796 |

## Závěry

- **Turnajová selekce** s vyšším tournsize (5) poskytla nejefektivnější konvergenci na optimální strategie.
- **Ruletová selekce** dosahuje středních výsledků, stále však lepších než náhodný výběr.
- **Náhodná selekce** (random) vede k nejhorším průměrným výsledkům a nevyužívá adaptivní potenciál algoritmu.

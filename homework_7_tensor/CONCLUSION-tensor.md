# Úkol 7 - Tensorflow

#### Daniel Král

v této práci předkládám souhrn mých pokusů s modely neuronových sítí, které jsem realizoval jako součást zadání. Abych pravdu řekl, moc tomu pořád nerozumím ale dal jsem něco s tutoriály dohromady...

## 1. Jednoduchý lineární model

- **Cíl**: Procvičit základy neuronových sítí na úloze předpovědi mzdy dle odpracovaných hodin.
- **Architektura**: Sekvenční model s jednou hustou (`Dense`) vrstvou o 1 neuronu.
- **Data**: Jednoduchá lehce se dají změnit, takže jsem mohl jednoduše posuzovat pŘesnost tréninku.

  - Vstupy: `hours = [2, 5, 8]`
  - Cílové hodnoty: `pay   = [30, 75, 120]`

- **Trénink**: 100 epoch

  - Použitý optimalizátor: **SGD** (Stochastic Gradient Descent) – iterativní metoda pro určení optimálních vah sítě, která se při každé aktualizaci učí ze vzorku nebo malých batchů dat.
  - Ztrátová funkce: **MSE** (Mean Squared Error) – průměr čtverců rozdílů mezi skutečnou a predikovanou hodnotou, která penalizuje větší chyby kvadratikou.

- **Výsledek**: Model se naučil přibližný vztah
  $pay ≈ 15 × hours + 0$
  což odpovídá očekávání a potvrdilo mi pochopení gradientního sestupu a ladění váh.

## 2. Classifikace květin Iris

Tento druhý pokus jsem dělal podle tutoriálu který jsem přepoužil na jiná data. (tyto data)

- **Datová sada**: Iris (150 vzorků) z `tensorflow_datasets`.
- **Rysy**: Délka a šířka dvou různých druhů lístků (celkem 4 rysy).
- **Třídy**: Tři druhy květin (setosa, versicolor, virginica).
- **Rozdělení**: 60 % trénink, 20 % validace, 20 % test.
- **Model**: Jedna skrytá vrstva s proměnným počtem jednotek a softmax výstup.
- **Hyperparametry GA**:

  - Počet jednotek ve skryté vrstvě (`HIDDEN_SIZES` = \[4, 8, 16, 32]).
  - Rychlost učení (`LEARNING_RATES` = \[0.01, 0.005, 0.001]).
  - GA parametry: populace 12, 4 generace, crossover 0.6, mutace 0.3.

- **Výsledek**: Po několika neúspěšných pokusech se podařilo dosáhnout **validacní přesnosti 90–97 %**.

## Závěr

1. **Jednoduchý první experiment** s lineárním modelem ukázal, že i pár řádek z knihovny keras dělá divy :D .
2. **Iris dataset** představuje vhodný příklad pro klasifikaci s malým počtem vzorků a rysů.
3. **GA pro ladění hyperparametrů** umožnilo automaticky nalézt dobrou kombinaci skryté vrstvy a rychlosti učení.
4. **Výkon** konečného modelu (90–97 % přesnosti) potvrzuje, že i jednoduchá architektura dokáže na kvalitních datech podávat vynikající výsledky.

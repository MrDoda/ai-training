# Úkol 4 - Generování terénu

#### Daniel Král

v následujícím dokumentu přináším formální přehled výsledků mého evolučního algoritmu a nejdůležitější závěry vyplývající z provedených testů.

## Klíčové poznatky

1. **TARGET_LAKES** (konfigurace _lakes_plus_)

   - Zvýšení hodnoty `TARGET_LAKES` z 2 na 3 vedlo ke zlepšení průměrné fitness z přibližně –3,35 na –2,35.
   - Chyba při počítání jezer (lake error) se snížila přibližně o 1, což potvrzuje, že algoritmus lépe dosahuje vyššího cílového počtu jezer.

2. **TARGET_VARIABILITY** (konfigurace _var_plus_)

   - Změna cílové standardní odchylky `TARGET_VARIABILITY` na 0,3 výrazně zvýšila chybu v počtu jezer na hodnotu 5.
   - Celková fitness poklesla, což naznačuje, že vyšší variabilita je pro algoritmus obtížně dosažitelná bez negativního dopadu na ostatní metriky.

3. **TARGET_FLOOD_RATIO** (konfigurace _flood_plus_)

   - Posunutí `TARGET_FLOOD_RATIO` na 0,9 vedlo ke zdvojnásobení chyby zaplavené oblasti (flood error) z 0,12 na přibližně 0,24.
   - Ostatní chyby (jezera, variabilita) zůstaly na srovnatelné úrovni, výsledná fitness tedy zůstala obdobná jako u základní konfigurace.

4. **USE_FLOOD** (konfigurace _use_flood_)

   - Aktivace parametru `USE_FLOOD` donutila algoritmus optimalizovat i poměr zaplavené plochy.
   - Chyba zaplavení spadla z 0,12 na 0,0067, zatímco odchylka variabilita se mírně zvýšila.
   - Celková fitness se změnila minimálně, protože váha této chyby je srovnatelná s ostatními.

5. **POP_SIZE** (konfigurace _pop_large_)

   - Zvýšení velikosti populace vedlo k mírnému zlepšení průměrné fitness díky lepší průzkumnosti prostoru řešení.
   - Tento přínos je vykoupen zvýšenými výpočetními nároky.

## Závěry

Na základě provedených experimentů můžeme konstatovat následující:

- Zvýšení hodnoty `TARGET_LAKES` (konfigurace _lakes_plus_) vedlo ke snížení chyby v počtu jezer (lake error) a zlepšení průměrné fitness.
- Změna `TARGET_VARIABILITY` na vyšší hodnotu (konfigurace _var_plus_) výrazně zvýšila chybu v počtu jezer a snížila celkovou fitness, což znamená, že vyšší variabilita je pro algoritmus obtížně dosažitelná.
- Posunutí `TARGET_FLOOD_RATIO` na 0,9 (konfigurace _flood_plus_) zdvojnásobilo chybu zaplavené plochy, aniž by ovlivnilo chyby v ostatních metrikách.
- Aktivace parametru `USE_FLOOD` (konfigurace _use_flood_) dramaticky snížila chybu zaplavené oblasti, zatímco ostatní chyby zůstaly téměř beze změny.
- Zvýšení velikosti populace (`POP_SIZE`) vedlo k mírnému zlepšení průměrné fitness díky lepší diverzitě, avšak za cenu vyšší výpočetní náročnosti.

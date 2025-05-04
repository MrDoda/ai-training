# Úkol 6 - Boom divers!

#### Daniel Král

v tomto dokumentu předkládám podrobný přehled klíčových částí kódu, metod a dosažených výsledků při evoluci neuronové sítě pro simulaci potápěče, jehož úkolem bylo vyhýbat se bombám a přežít co nejdéle.

---

## 1. Senzorické funkce (`get_sensor_inputs`)

| Index | Popis                                                                  | Interval |
| ----- | ---------------------------------------------------------------------- | -------: |
| 0     | Vzdálenost k nejbližší mine (normovaná podle maximální diagonály mapy) |   ⟨0, 1⟩ |
| 1     | Δx k cíli (flag) / WIDTH (–1 je vlevo, +1 je vpravo)                   |  ⟨–1, 1⟩ |
| 2     | Δy k cíli (flag) / HEIGHT (–1 je nahoře, +1 je dole)                   |  ⟨–1, 1⟩ |
| 3     | Vzdálenost od levé stěny / WIDTH                                       |   ⟨0, 1⟩ |
| 4     | Vzdálenost od horní stěny / HEIGHT                                     |   ⟨0, 1⟩ |

---

## 2. Neural network forward pass (`nn_function`)

- **model**: jednovrstvý perceptron s 5 vstupy + bias → 4 výstupy (směr pohybu: nahoru, dolů, doleva, doprava).

---

## 3. Navigace agenta (`nn_navigate_me`)

- Ze sítí získáme čtyři výstupy, z nichž vybereme index `i = argmax(out)`:

  - 0 → pohyb **nahoru**
  - 1 → pohyb **dolů**
  - 2 → pohyb **doleva**
  - 3 → pohyb **doprava**

- Poloha agenta se aktualizuje o konstantní rychlost **ME_VELOCITY** a zároveň se inkrementuje ujetá vzdálenost pro penalizaci nečinnosti.

---

## 4. Fitness funkce (`handle_mes_fitnesses`)

Fitness každého agenta `me.fitness` se skládá ze čtyř složek:

1. **Doba přežití** (`base_fit = me.timealive`).
2. **Bonus za dosažení cíle** (`win_bonus = 1000`, pokud `me.won == True`).
3. **Penalizace pasivity**:

   - `moves_made = me.dist / ME_VELOCITY`
   - `stationary_ticks = me.timealive − moves_made`
   - `idle_penalty = 2 × stationary_ticks`

4. **Penalizace vzdálenosti od cíle**:

   - `dist_to_flag = hypot(delta_x, delta_y)`
   - `dist_penalty = (dist_to_flag / MAX_DIST) × 500`

**Konečná fitness**:

```
me.fitness = base_fit
               + win_bonus
               - (0 if won else idle_penalty)
               - (0 if won else dist_penalty)
```

Tímto způsobem agenti jsou motivováni přežít, rychle se hýbat a dostat se co nejblíže k praporci.

---

## 5. Závěr

Nejvíce jsem experimentoval se změnami Fitness funkce, rozpohybovat potápěče aby jen nestáli v rohu dalo zabrat.

I tak by ta funkce mohla být lepší, ale s populací 1000 to trvá asi jen cca 10 generací než se naučí běhat k vlajce :D

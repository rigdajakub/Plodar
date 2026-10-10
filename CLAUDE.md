# Pokyny pre Claude

Používateľ je Jakub. Komunikuj po slovensky.

## Dizajnový koncept (platí pre prezentácie, aplikácie, stránky a všetko nové)

Všetko, čo používateľ nechá vytvoriť, robím na rovnaký alebo podobný koncept ako
`Jakub/projekty/AI_prezentacia_5_slidov.html`. Ak používateľ výslovne požiada o niečo iné
(iné farby, iný štýl), splním to, ale držím sa podobného konceptu.

- **Štýl:** inšpirovaný consulting.com. Čisto čierne pozadie, tmavé panely (#0F0F0F) s jemným okrajom,
  veľa voľného priestoru, centrované nadpisy, prémiový a minimalistický vzhľad.
- **Farby:** magenta (#E20074) ako jediný akcent, čierna, biela. Zlatú z consulting.com nepoužívať.
  Magenta len na zvýraznenia, čísla, čiary, ikony a tlačidlá s prechodom.
- **Písmo:** Inter (text, tlačidlá), Instrument Sans (čísla a dashboard prvky), nadpisy v seriferovom
  písme: Tiempos Headline Light, ak je dostupné, inak Newsreader (bezplatná náhrada).
  Nadpisy majú sivo-biely prechod a jemný magentový lesk.
- **Prvky:** horný navigačný pás s aktuálnou sekciou, skleněné dlaždice so štatistikami, karty s malou
  magentovou čiarkou hore, tlačidlá s prechodom do magenty, ikony s magentovým prechodom.
- **Animácie:** vždy aspoň 1 – 2 na každom slide alebo sekcii. Prvky sa postupne zaostrujú
  (blur-in), čísla nabiehajú, grafy a čiary sa vykresľujú, pomalé pohyblivé pozadie.
  Nič rýchle ani blikajúce. Rešpektovať `prefers-reduced-motion`.
- **Prezentácie:** 1920×1080, v slovenčine, text stručný, k slidu poznámky pre rečníka, zdroj malým písmom
  pri každom čísle. Ovládanie: šípky, `N` poznámky, `P` režim rečníka, `O` prehľad, `F` celá obrazovka,
  `B` stmavenie, tlač do PDF.

## Pravidlá kvality

- **Čísla a fakty:** len overené, z primárnych zdrojov (Eurostat, WEF, MMF, OECD, EUR-Lex, Stanford a pod.).
  Nič nevymýšľať. Čo sa nedá overiť, výslovne napísať.
- **Bez chýb:** výsledok vždy vykresliť v headless Chromium (Playwright) a skontrolovať pretečenie textu,
  konzolu, mobil a tlač, až potom odovzdať.
- Bez log a značiek firiem.
- Výstup uložiť do `Jakub/projekty/`, zverejniť ako Artifact a pridať do PR vetvy.

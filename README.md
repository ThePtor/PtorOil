# PtorOil
Zápočtový program
# Uživatelská dokumentace
## Jak spustit program
Program lze spustit buďto přiloženým dávkovacím souborem, nebo přes příkazovou řádku spuštěnou z hlavní složky programu pomocí příkazu

    python3 ./python/PtorOil.py

Toto bude fungovat za předpokladu, že jsou nainstalované moduly pythonu uvedené v souboru 

    ~/PtorOil-main/python/requirements.txt
## Úvodní obrazovka
**Quick game** - spustí jedno herní kolo s náhodně vybraným seedem

**Quit** - ukončí okno

## Herní kolo
**Datum a cena ropy** - ukazuje současné datum a aktuální cenu ropy za barel, cena ropy se mění v čase i následkem hráčových akcí

**Peníze** - hráčovy aktuální peníze, které lze utratit, na konci kola 

**Hledači** - 1 hledač umožňuje prohledat jedno pole mapy zdarma, v průběhu kola hráč získává hledače automaticky

### Mapa
Na polích mapy hráč hledá a těží ropu, zpočátku je celá mapa skrytá. Kliknutím na prázdné pole odhalí hráč jeho kvalitu. Kliknutím na odhalené pole se přepne do režimu stavby a může na daném poli postavit jednu ze svých těžebních věží. Při opětovném kliknutí na téže pole se režim stavby vypne. Při kliknutí na jiné odhalené pole se vybere pro stavbu toto nové pole. Po zničení věže se odhalí množství ropy na poli a z pole už nelze dále těžit.
 
#### Kvalita a množství ropy
Kvalita pole určuje jakou rychlostí bude těžit věž postavená na vybraném poli (zelená - nízká kvalita, modrá - vysoká kvalita).

Množství ropy určuje, kolik ropy je nejvýše možné z pole vytěžit.

Kvalita a množství ropy jsou na sobě nezávislé.

### Stavby
#### Silo
Silo ukládá vytěženou ropu do limitu své kapacity, ukazuje stav naplnění.  jestliže do plného sila přiteče další tato ropa se neuloží ale silo může přetéct (což sníží skóre).

**Limit přetečení** - určuje, jak dlouho vydrží plné silo než přeteče

**Kapacita** - kapacita sila

#### Kůň
Koně vozí ropu do města, odveze maximální možné množství ropy ze sila. Ve městě prodá svůj náklad za aktuální cenu ropy.

**Doba cesty** - jak dlouho trvá koni cesta do města a zpět (2/3 z doby je cesta do města, 1/3 z doby je cesta zpět) 

**Kapacita** - maximální náklad vozu

#### Těžební věž
Těžební veže těží ropu z polí na kterých jsou postavené. Rychlost těžby věže je mj. ovlivněna kvalitou pole, na kterém se věž nachází.

**Rychlost těžby** - vylepšení základní rychlosti těžby

**Efektivita** - poměr mezi množstvím ropy, které věž vytěží a které ubyde ze zásob v poli

## Vstupní data
Vstupními daty je klikání na tlačítka za účelem získání co nejvyššího skóre. Způsob jakým je možné tohoto dosáhnout je ponechán na hráči.

## Výstupní data
Výstupními daty je jedna hodnota typu float, která značí dosažené skóre.

## Co se nestihlo (došla vůle)
Není doděláno ukládání jakýchkoliv savů, takže hra je 100% arkádová. Také není hotová možnost vytvořit si hru s vlastními vstupními parametry. Zpřehlednění a vyšší efektivita je také možná. 

Chybí ošetřit některé případy, kdy jsou poškozené jiné herní soubory(nelze najít obrázky atp.) 

### Jak dodělat to, co se nestihlo
Možnost vytvořit si hru podle vlastních parametrů by zahrnovalo vytvoření další obrazovky, kam hráč zadá požadované úpravy své hry, a jejich načtení do proměnnýchh používaných pro hru.

Pro ukládání savů je potřeba implementovat způsob, jak uložit a načíst pole pozemků, aby zůstaly jejich hodnoty ve stejném stavu po načtení jako byly při uložení.

Prostor pro zefektivnění je snížení počtu slovníku z počtu množství vylepšovatelných stavech na jeden vzorový pro každý druh stavby, ze kterého se  by se čerpaly hodnoty příslušné pro každý level upgradu. 

# ToDo list
- [ ] Dostat zápočet

## Neprogramování
- [x] Playtesting
- [x] Balancování
- [x] Hezké obrázky

## Programování
- [ ] Práce s vnějšími soubory
- [ ] Okno GUI
- [ ] Setup screen
- [x] Herní kolo

### Práce s vnějšími soubory
- [x] Čtení a zápis config souborů
- [ ] *Optional: Čtení a zápis ze save souborů*
- [ ] *Optional: Zápis do leaderboard soborů*
- [ ] *Optional: Save on exit*

### Okno GUI
- [x] Rozdělení okna na panely
- [ ] Automatický resize podle velikosti
- [ ] Settings panel

### Setup screen
- [ ] Výběr seedu
- [ ] Startovní sekvence
- [ ] *Optional: Načíst hru ze souboru*

### Herní kolo
- [x] Implementace náhodných funkcí - perlin noise
- [x] Timer kola
- [x] Fungování ingame ekonomiky
- [x] Objekty
- [x] Grafika

### Objekty
- [x] Ropná věž
- [x] Kůň
- [x] Políčka na mapě
- [x] Ropné silo

#### Ropná věž
- [x] Okénko s věží
- [x] Umí se postavit na políčku
- [x] Těžba ropy
- [x] *Optional: Upgrady - rychlost těžby*
- [x] Zbourej věž

#### Kůň
- [x] Okénko s koněm
- [x] Naber ropu ze sila
- [x] Ve městě prodej ropu
- [x] *Optional: Upgrady - rychlost koně, kapacita cisterny*

#### Políčka na mapě
- [x] Generátor políček s rozdělením ropy
- [x] Prohledej políčko
- [ ] *Optional: Upgrady hledání políček*
- [x] Postav na políčku věž, odstraň z políčka věž

#### Ropné silo
- [x] Okénko se silem
- [x] Silo ukazuje stav naplnění
- [x] Příbytek a úbytek ropy
- [x] *Optional: Pokuta za přeplnění sila*
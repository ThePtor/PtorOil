# PtorOil
Zápočtový program
# Uživatelská dokumentace
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

# Neuživatelská dokumentace
## Struktury v programu
### Class: Tile
Vlastní struktura pro políčka na mapě, každé z nich má dva hlavní atributy *quality* a *oil*, které určují kvalitu daného pole, respektive množství ropy v poli. Mapa se sestává z dvourozměrného sezamu těchto polí, u nichž jsou jejich atributy určeny pomocí knihovny PerliNoise, která generuje náhodné hodnoty obou atributů ze zadaného seedu a jejich pozice v tomto seznamu.

### Class: Upgrade
Druhá vlastní struktura, pro vylepšitelné stavby ve hře. Ty obsahují reprezentaci svého obsahu pomocí Tkinter. Jejich atributy jsou uloženy ve slovníku *stats*,  který obshuje vnořené slovníky pro jednotlivé proměnné. Tato třída je při inicializaci upravena ze základního vzoru pro potřeby jednotlivých druhů staveb. Struktura upgradů lze nastavit přes konfigurační soubory .json s odpovídajícím názvem upgradu, ty mají přednost při načítání konfigurace před přednastavenými vzory.

### Slovníky
Slovníky slouží jednak k ukládání proměnných, ale druhak i k centralizaci programu, kdy je veškerý text soustředěn do slovníků pro jednoduchost úprav.

## Vybrané funkce
### gametick()
Funkce která spravuje veškerý posun v čase o jeden den vpřed. Od úpravy ceny a data po těžbu a prodej ropy. Běží na vlastním vlákně do doby, než je zavřeno okno nebo než hra skončí.

### correct_price()
Funkce, která spravuje cenu ropy na trhu. Cena se skládá z náhodné složky, opět přes PerlinNoise, ale hráč také dočasně snižuje cenu ropy tím, že ji prodává. V moment prodeje se množství prodané ropy exponenciální ryclostí dostává na trh, v důsledku čehož klesá cena. Se zpožděním ropa z trhu mizí, rychlostí podstatně nižší, v důsledku čehož cena opět stoupá zpět na základní hodnotu náhodné složky.

## Vstupní data
Vstupními daty je klikání na tlačítka za účelem získání co nejvyššího skóre

## Výstupní data
Výstupními daty je jedna hodnota typu float, která značí dosažené skóre.

# ToDo list
- [ ] Dostat zápočet

## Neprogramování
- [ ] Playtesting
- [ ] Balancování
- [ ] Hezké obrázky

## Programování
- [ ] Práce s vnějšími soubory
- [ ] Okno GUI
- [ ] Setup screen
- [ ] Herní kolo

### Práce s vnějšími soubory
- [ ] Čtení a zápis config souborů
- [ ] *Optional: Čtení a zápis ze save souborů*
- [ ] *Optional: Zápis do leaderboard soborů*
- [ ] *Optional: Save on exit*

### Okno GUI
- [ ] Rozdělení okna na panely
- [ ] Automatický resize podle velikosti
- [ ] Settings panel

### Setup screen
- [ ] Výběr seedu
- [ ] Startovní sekvence
- [ ] *Optional: Načíst hru ze souboru*

### Herní kolo
- [ ] Implementace náhodných funkcí - perlin noise
- [ ] Timer kola
- [ ] Fungování ingame ekonomiky
- [x] Objekty
- [ ] Grafika

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
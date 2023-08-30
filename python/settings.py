# Starting settings for main python file
money = 2500 #starting money
dowsers = 3 #starting dowsers
dowserdelay = 15 #delay between free dowsers
yearlen = 365 # length of game in days
gamespeed = 1 # speed of game (days/s)
plot_base = 1000 #reveal price without dowser
plot_price = 0 #starting plot purchase price
seed = 3 # default seed
spillage_severity = 40 #spilage fine per barel spilled
mining_speed = 0.7 # global mining speed
oil_richness = 1 # global oil field richness
mapsize = 10 # size of oil map
demand = 0 #speed of price recovery after selling oil
demand_step = 0.01 #effect of upgrade on price recovery
pricedrop = 0.3 #how much sold barrel affects price ($/barrel)

# Language dictionaries
msg_general = {
    "jan" : "Leden",
    "feb" : "Únor",
    "mar" : "Březen",
    "apr" : "Duben",
    "may" : "Květen",
    "jun" : "Červen",
    "jul" : "Červenec", 
    "aug" : "Srpen",
    "sep" : "Září", 
    "oct" : "Říjen", 
    "nov" : "Listopad",
    "dec" : "Prosinec",
    "bar" : "barelů",
    "day" : "dní",
    "available" : "Dostupní hledači:",
    "plot" : "Cena za prohledání:",
    "total_mined" : "Vytěžená ropa:",
    "total_sold" : "Prodaná ropa:",
    "spillage_fine" : "Rozlitá ropa:",
    "loan" : "Výše půjčky:",
    "money" : "Peníze:",
    }

msg_horse = {
    "name" : "Kůň",
    "buy": "Koupit koně",
    "upgrade": "Upgrade",
    "speed" : "Doba cesty: ",
    "capacity" : "Kapacita: ",
    "sell_cmd" : "Prodat ropu!",
    "forward" : "Na cestě do města.",
    "back" : "Na cestě zpět.",
    "max_level" : "MAXLEVEL",

}

msg_rig = {
    "name" : "Těžební věž",
    "buy" : "Koupit novou věž",
    "destroy" : "Zničit věž",
    "build" : "Postavit věž",
    "upgrade" : "Upgrade", 
    "speed" : "Rychlost těžby:",
    "capacity" : "Efektivita: ",
    "quality" : "Kvalita pozemku: ",
    "cur_speed" : "Aktuální rychlost těžby: ",
    "max_level" : "MAXLEVEL",

}

msg_silo = {
    "name" : "Silo na ropu",
    "upgrade" : "Upgrade",
    "speed" : "Limit přetečení: ",
    "capacity" : "Ropa: ",
    "max_level" : "MAXLEVEL",

}
# Tady nekdy bude program
import json
import threading
import time
import random
from tkinter import *
from PIL import Image, ImageTk
from perlin_noise import PerlinNoise
from matplotlib import pyplot as plt


class Tile:
    """Class for oil tiles on map"""
    def __init__(self, master, position, oil, quality) -> None:
        
        self.but = Button(master, command=self.reveal, width=6*baseunit, height=6*baseunit, image=emptyim, compound='bottom', padx=0, pady=0)
        
        self.active = False
        self.pos = position
        self.oil = oil
        self.qual = quality
        self.mineable = False
        self.but.grid(row=self.pos[0], column=self.pos[1])
    def reveal(self):
        self.but.config(background="green", text=f"{self.qual:.2f}")
        self.mineable = True
        self.but.config(command=self.tile_pass)
        
    def tile_pass(self):
        global pos_cache
        if pos_cache == self.pos:
            pos_cache = None
            self.but.config(background="green")
        else:
            if pos_cache:
                oil_fields[pos_cache[0]][pos_cache[1]].but.config(bg="green")
            pos_cache = self.pos
            self.but.config(background="blue")
        toggle_rigs()


class Upgrade:
    """Class for upgradable buildings - horse, silo, mining rig."""
    def __init__(self, master, version, number=0) -> None:
        self.box = Frame(master)
        self.b_build = Button(self.box, image=emptyim, compound="bottom")
        self.b_upgrade1 = Button(self.box) #image=emptyim, compound="bottom")
        self.b_upgrade2 = Button(self.box) #image=emptyim, compound="bottom")
        self.b_send = Button(self.box, image=emptyim, compound="bottom")
        self.text = Label(self.box, background="#00FFFF")
        self.l_upgrade1 = Label(self.box, background="#FF00FF")
        self.l_upgrade2 = Label(self.box, background="#FF00FF")
        self.l_description1 = Label(self.box)
        self.l_description2 = Label(self.box)
        self.icon = PhotoImage()
        self.version = version
        self.names = dict
        self.cost = int
        self.column = number
        self.stats  = {"speed" : {"level": 0, "val": [15, 10, 6, 4, 3], "price": [0, 1999, 5000, 6900, 12300]}, #speed/mining speed
                       "capacity" : {"level": 0, "val": [0, 1, 2, 500, 56], "price": [250, 500, 1000, 250, 600]}, #capacity/mining effectivity
                       "quality" : 0, #plot quality
                       "oil" : 200, #remaining oil
                       "cur_speed" : 0, #current mining speed
                       } 
        self.timer  = 0
        self.upgrades = int
        self.pos = (-1,-1)
        self.available = False
        self.active = False
        self.assign_type(version)
        self.activate()
       
    def assign_type(self, version):
        """Assigns default values based on type of builidng"""
        possible = {"horse": self.horse,
                    "silo": self.silo,
                    "rig": self.rig}
        possible[version]()

    def assign_image(self):
        """Assigns image according to version and upgrade level"""

    def activate(self):
        """Packs upgrade box into Tk window"""
        self.box.grid(column=self.column, row=0)
        self.box.grid_rowconfigure(0, weight=1)
        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid(sticky="we")
        

    def dig_oil(self):
        """Rig function that digs oil"""
        pass

    def sell_oil(self):
        """Horse function that sells oil."""
        global money, soldoil
        profit = self.stats['oil'] * price
        soldoil += self.stats['oil']
        self.stats['oil'] = 0
        money += profit
        moneycounter.config(text=f"${money:.0f}")
        return profit
    
    def spillage(self):
        """Silo function that fines player if silo overflows."""
        pass

    def buy(self, first=False):
        """Function that buys selected Upgrade instance, if first is True buying is free."""       
        toggle = False
        if first:
            toggle = True
        if not toggle:
            toggle = check_money(self.stats['capacity']['price'][0])
        if toggle:
            self.available = True
            self.b_build.grid_remove()
            self.l_upgrade1.grid(row=1, column=0, sticky="w")
            self.b_upgrade1.grid(row=1, column=1)
            self.l_upgrade2.grid(row=2, column=0, sticky="w")
            self.b_upgrade2.grid(row=2, column=1)
            if self.version != "silo":
                self.b_send.grid(row=3, column=0, columnspan=2)

            if self.version == "rig":
                self.l_description1.grid(row=4, column=0, columnspan=2)
                self.l_description2.grid(row=5, column=0, columnspan=2)
                toggle_rig(self)
    

    def build_rig(self):
        # Builds mining rig and enables mining funcitonality.
        global pos_cache
        # Načte rozkliklé pole s ropou
        tile = oil_fields[pos_cache[0]][pos_cache[1]]
        tile.but.config(state=DISABLED, bg="yellow") #Vypne a označí pole s ropou
        
        self.pos = pos_cache # Do své pozice nastaví odkaz na pole s ropou které těží
        pos_cache = None # Resetuje označené pole 
        self.available = False # Vypne svou dostupnost
        self.active = True # Marker pro těžební funkci
        self.b_send.config(text=self.names['destroy'], fg="red", command=self.destroy_rig)
        
        self.stats['quality'] = tile.qual
        self.stats['oil'] = tile.oil
        toggle_rigs()
        self.l_description1.config(text=f"{self.names['quality']} {self.stats['quality']:.2f}")
    
    def destroy_rig(self):
        self.stats['quality'] = 0
        self.stats['cur_speed'] = 0
        self.update_text()
        self.b_send.config(text=self.names['build'], fg="black", command=self.build_rig)
        
        oil_fields[self.pos[0]][self.pos[1]].but.config(bg="magenta")
        self.pos = (-1, -1)
        self.available = True
        self.active = False
        toggle_rig(self)

    def update_text(self):
        """Intentionally empty placeholder function"""
        pass


    def level_up(self, upgradename):
        if check_money(upgradename['price'][upgradename['level']+1]):
            upgradename['level'] += 1
            self.update_text()
            moneycounter.config(text=f"${money:.0f}")

    def goto_city(self):
        """does one step towards city to sell oil"""
        self.timer -= 1
        if self.timer <= 0:
            self.kill_horse()
        elif self.timer <= (self.stats['speed']['val'][self.stats['speed']['level']]/3):
            self.b_send.config(text=f"{self.names['back']} ({self.timer} dní)")
        elif self.timer <= (self.stats['speed']['val'][self.stats['speed']['level']]/3 + 1):
            self.b_send.config(text=f"+${self.sell_oil()}")
        else:
            self.b_send.config(text=f"{self.names['forward']} ({self.timer} dní)")
        #UNFINISHED
        print(self.timer)
    

    def kill_horse(self):
        self.active = False        
        self.b_send.config(text=self.names['sell_cmd'], state=ACTIVE)
        # UNFINISHED

    def horse(self) -> None:
        """Sets default values for the "horse" type of upgrade."""

        def horse_go():
            """Switches horse into active state!"""
            self.active = True
            self.timer = self.stats['speed']['val'][self.stats['speed']['level']]
            amt = min(self.stats['capacity']['val'][self.stats['capacity']['level']], oil_silo.stats['oil'])
            self.stats['oil'] = amt
            oil_silo.stats['oil'] -= amt
            oil_silo.update_text()
            self.b_send.config(state=DISABLED, text=f"{self.names['forward']}")
            # UNFINISHED            

        #self.stats = horse_stats
        self.names = msg_horse
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))
        self.b_send.config(text=self.names['sell_cmd'], command=horse_go)
        self.b_build.config(text=f"{self.names['buy']}\n(${self.stats['capacity']['price'][0]})", command=self.buy)

        def txt():
            # self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']} s", justify="left")
            # self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']} barelů", justify="left")
        
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]} dní", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']['val'][self.stats['capacity']['level']]} barelů.", justify="left")
            if self.stats['speed']['level'] < levelcap:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < levelcap:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)

        self.update_text = txt
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2) 


    def silo(self) -> None:
        """Sets default values for the "silo" type of upgrade."""
        self.names = msg_silo    
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        #self.stats = silo_stats

        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))

        

        def txt():
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]:.2f} x", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['oil']}/{self.stats['capacity']['val'][self.stats['capacity']['level']]} bar", justify="left")

            if self.stats['speed']['level'] < 2*levelcap:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < 2*levelcap:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)


        self.update_text = txt
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2)

    def rig(self) -> None:
        """Sets default values for the "rig" type of upgrade."""
        # self.stats = rig_stats
        self.names = msg_rig    
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        
        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))
        self.b_send.config(text=f"{self.names['build']}", command=self.build_rig)
        self.b_build.config(text=f"{self.names['buy']}\n(${self.stats['capacity']['price'][0]})", command=self.buy)

        

        def txt():
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]:.2f} x", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']['val'][self.stats['capacity']['level']]} %", justify="left")
            self.l_description1.config(text=f"{self.names['quality']} {self.stats['quality']:.2f}")
            self.l_description2.config(text=f"{self.names['cur_speed']} \n{self.stats['cur_speed']} bar/den")
            if self.stats['speed']['level'] < levelcap:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < levelcap:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)


        self.update_text = txt
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2)

    


def toggle_rigs():  
    for well in rig_field:
        if well.available:
            toggle_rig(well)

def toggle_rig(obj:Upgrade):
    if pos_cache:
        obj.b_send.config(state=ACTIVE)
    else:
        obj.b_send.config(state=DISABLED)

def check_money(price):
    """Checks if player has enough money, if so, subtracts that amount from player and returns True"""
    global money
    if price <= money:
        money -= price
        moneycounter.config(text=f"${money:.0f}")
        return True
    else:
        return False
    
def update_price():
    global pricedelta, price
    r_price = noise((-1,-1, 3*day/yearlen))
    price = 50 + (100*r_price + pricedelta)
    cur_price.config(text=f"${price:.2f}/bar")
    
def gametick():
    global day
    day += 1
    # for rig in rig_field:
    #     if rig.active:
    #         rig.dig_oil()
    for hrs in herd:
        if hrs.active:
            hrs.goto_city()
    update_price()

    time.sleep(1/5)
    
def timer():
    while not game_end.is_set():
        gametick()

msg_horse = {
    "name" : "Kůň",
    "buy": "Koupit koně",
    "upgrade": "Upgrade",
    "speed" : "Doba cesty: ",
    "capacity" : "Kapacita nákladu: ",
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


unitsize = 8
cfg_values = json.load(open("./data/config.json","r", encoding="UTF-8"))
print(cfg_values["sizex"])
# config = {"riglimit" : 5}
# rigs = [0,1]
# riglimit = 5
# okno = Tk()
# x = Tile(okno, (0,0), 1500, 5)
# okno.mainloop()

#Default variables

mainframe = Tk()

map_frame = Frame(mainframe)
rig_frame = Frame(mainframe)
horse_frame = Frame(mainframe)
silo_frame = Frame(mainframe)
emptyim = PhotoImage()
game_end = threading.Event()

baseunit = 5
day = 0
yearlen = 365
#Startup variables
money = 20000
moneycounter = Label(mainframe, text=f"${money:.0f}", font=("Algerian", 35))
pricedelta = 0
price = 0

cur_price = Label(mainframe, text=f"${price:.2f}/bar", font=("CMU Serif", 24))
soldoil = 0
oilbuffer = 0
spillage_severity = 1
levelcap = 2
seed = 3
mapsize = 10
pos_cache = None
# noise = PerlinNoise(2, seed)
noise = PerlinNoise(4, random.random())
oil_fields = [[Tile(map_frame, (x,y), 500, noise([x/mapsize,y/mapsize])) for y in range(mapsize)] for x in range(mapsize)]

# x = Upgrade(y, "horse", 1)
# x2 = Upgrade(y, "horse", 2)

moneycounter.grid(column=1, columnspan=1, row=0)
cur_price.grid(column=1, row=1)
silo_frame.grid(column=2, row=0, rowspan=2)
map_frame.grid(column=0, row=0, rowspan=5)
horse_frame.grid(column=1, row=2)
rig_frame.grid(column=1, row=3)

oil_silo = Upgrade(silo_frame, "silo")
oil_silo.buy(True)
herd = [Upgrade(horse_frame, "horse", x) for x in range(5)]
herd[0].buy(True)
rig_field = [Upgrade(rig_frame, "rig", x) for x in range(5)]
rig_field[0].buy(True)

# print(x.cost)
# print(cfg_values)
update_price()
t1 =  threading.Thread(target=timer)
t1.start()
mainframe.mainloop()
game_end.set()
print("69")
# vallist = [50+75*noise((-1,-1,(2*x)/yearlen))+25*noise((11,11,(5*x)/yearlen)) for x in range(yearlen)]
# print(sum(vallist)/len(vallist))
# plt.plot([x for x in range(yearlen)], vallist)
# plt.show()

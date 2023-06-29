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
        
        self.but = Button(master, command=self.reveal, width=3, height=3)
        
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
    def __init__(self, master, version, number) -> None:
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
        self.stats  = {"speed" : 150, #speed/mining speed
                       "price_1" : 1500, #speed price
                       "level_1" : 0, #upgrade level 1
                       "capacity" : 20, #capacity/mining effectivity
                       "price_2" : 2500,  #level, capacity price
                       "level_2": 0, #upgrade level 2
                       "quality" : 0, #plot quality
                       "oil" : 0, #remaining oil
                       "cur_speed" : 0, #current mining speed
                       } 
        self.upgrades = int
        self.pos = (-1,-1)
        self.level = 1
        self.available = False
        self.active = False
        self.assign_type(version)
        self.activate()
       

    def assign_type(self, version):
        """Assigns default values based on type of builidng"""
        possible = {"horse": horse,
                    "silo": silo,
                    "rig": rig}
        possible[version](self)

    def assign_image(self):
        """Assigns image according to version and upgrade level"""

    def activate(self):
        """Packs upgrade box into Tk window"""
        self.box.grid(column=self.column, row=0)
        self.box.grid_rowconfigure(0, weight=1)
        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid(sticky="we")
        

    def dig_oil(self):
        pass

    def buy(self):       
        self.available = True
        self.b_build.grid_remove()
        self.l_upgrade1.grid(row=1, column=0, sticky="w")
        self.b_upgrade1.grid(row=1, column=1)
        self.l_upgrade2.grid(row=2, column=0, sticky="w")
        self.b_upgrade2.grid(row=2, column=1)
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
        self.l_description1.config(text=f"{self.names['quality']} {self.stats['quality']:.2f}")
        self.l_description2.config(text=f"{self.names['cur_speed']} \n {self.stats['cur_speed']:.2f} bar/den")
        self.b_send.config(text=self.names['build'], fg="black", command=self.build_rig)
        
        oil_fields[self.pos[0]][self.pos[1]].but.config(bg="magenta")
        self.pos = (-1, -1)
        self.available = True
        self.active = False
        toggle_rig(self)

    def update_text(self):
        pass


    def level_up(self, upgradename, price, level, but:Button):
        self.stats[level] += 1
        self.stats[price] *= 10
        self.stats[upgradename] += 20
        if self.stats[level] < levelcap:
            but.config(text=f"{self.names['upgrade']}\n(${self.stats[price]})")
        self.update_text()



def horse(obj:Upgrade) -> None:
    """Sets default values for the "horse" type of upgrade."""
    def goto_city(event=game_end):
        """Sends horse to city with oil and sells it."""    
        pass

    def horse_go():
        """Starts thread that sends horse to town."""
        t1 = threading.Thread(target=goto_city)
        t1.start()
    obj.names = msg_horse
    obj.text.config(text=obj.names['name'], font=("Calibri", 18, "bold"), justify="center")
    obj.b_upgrade1.config(text=f"{obj.names['upgrade']} \n(${obj.stats['price_1']})", height=2)
    obj.b_upgrade2.config(text=f"{obj.names['upgrade']} \n(${obj.stats['price_2']})", height=2)
    obj.b_send.config(text=obj.names['sell_cmd'], command=horse_go)
    obj.b_build.config(text=obj.names['buy'], command=obj.buy)

    def txt():
        obj.l_upgrade1.config(text=f"{obj.names['speed']} \n{obj.stats['speed']} s", justify="left")
        obj.l_upgrade2.config(text=f"{obj.names['capacity']} \n{obj.stats['capacity']} barelů", justify="left")
    
    obj.update_text = txt
    obj.update_text()
    obj.text.grid(row=0, column=0, columnspan=2)
    obj.b_build.grid(row=1, column=0, columnspan=2) 


def silo(obj:Upgrade) -> None:
    """Sets default values for the "silo" type of upgrade."""
    pass

def rig(obj:Upgrade) -> None:
    """Sets default values for the "rig" type of upgrade."""
    obj.names = msg_rig    
    obj.text.config(text=obj.names['name'], font=("Calibri", 18, "bold"), justify="center")
    
    obj.b_upgrade1.config(text=f"{obj.names['upgrade']} \n(${obj.stats['price_1']})", height=2, command=lambda: obj.level_up('speed','price_1','level_1', obj.b_upgrade1))
    obj.b_upgrade2.config(text=f"{obj.names['upgrade']} \n(${obj.stats['price_2']})", height=2, command=lambda: obj.level_up('capacity','price_2','level_2', obj.b_upgrade2))
    obj.b_send.config(text=f"{obj.names['build']}", command=obj.build_rig)
    obj.b_build.config(text=f"{obj.names['buy']}", command=obj.buy)

    

    def txt():
        obj.l_upgrade1.config(text=f"{obj.names['speed']} \n {obj.stats['speed']:.2f}x", justify="left")
        obj.l_upgrade2.config(text=f"{obj.names['capacity']} \n +{obj.stats['capacity']} %", justify="left")
        obj.l_description1.config(text=f"{obj.names['quality']} {obj.stats['quality']:.2f}")
        obj.l_description2.config(text=f"{obj.names['cur_speed']} \n {obj.stats['cur_speed']:.2f} bar/den")
    
    obj.update_text = txt
    obj.update_text()
    obj.text.grid(row=0, column=0, columnspan=2)
    obj.b_build.grid(row=1, column=0, columnspan=2)

    


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
    global money
    if price <= money:
        money -= price
        moneycounter.config(text=f"${money}")
        return True
    else:
        return False


msg_horse = {
    "name" : "Kůň",
    "buy": "Koupit koně",
    "upgrade": "Upgrade",
    "speed" : "Doba cesty: ",
    "capacity" : "Kapacita nákladu: ",
    "sell_cmd" : "Prodat ropu!",
    "selling" : "Na cestě do města.",
    "back" : "Na cestě zpět.",
    "max_level" : "Maximální \núroveň",
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
    "max_level" : "Maximální \núroveň",

}

msg_silo = {
    "name" : "Silo na ropu",
    "upgrade" : "Upgrade",
    "fill" : "Aktuální ropa: ",
    "capacity" : "Kapacita ropy: ",

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
emptyim = PhotoImage()
game_end = threading.Event()

#Startup variables

money = 2000
moneycounter = Label(mainframe, text=f"${money}", font=("Calibri", 35))
levelcap = 3
seed = 3
mapsize = 10
pos_cache = None
noise = PerlinNoise(3, seed)
oil_fields = [[Tile(map_frame, (x,y), 500, noise([x/mapsize,y/mapsize])) for y in range(mapsize)] for x in range(mapsize)]

# x = Upgrade(y, "horse", 1)
# x2 = Upgrade(y, "horse", 2)
moneycounter.pack()
map_frame.pack()
horse_frame.pack()
rig_frame.pack()

herd = [Upgrade(horse_frame, "horse", x) for x in range(5)]
herd[0].buy()
rig_field = [Upgrade(rig_frame, "rig", x) for x in range(5)]
rig_field[0].buy()


# print(x.cost)
print(cfg_values)
mainframe.mainloop()
game_end.set()
print("3")
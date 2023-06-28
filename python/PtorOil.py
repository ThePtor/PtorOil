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
        self.but.config(background="green", text="{:.2f}".format(self.qual))
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
        self.cost = int
        self.column = number
        self.stats  = {(1) : 150, #speed/mining speed
                       (2) : [1 ,1500], #level, speed price
                       (3) : 20, #capacity/mining effectivity
                       (4) : [1, 2500],  #level, capacity price
                       (5) : "n/a", #plot quality
                       (6) : 0 #current mining speed
                       } 
        self.upgrades = int
        self.pos = (-1,-1)
        self.level = 1
        self.available = False
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

def horse(obj:Upgrade) -> None:
    """Sets default values for the "horse" type of upgrade."""
    def goto_city(event=game_end):
        """Sends horse to city with oil and sells it."""    
        pass

    def horse_go():
        """Starts thread that sends horse to town."""
        t1 = threading.Thread(target=goto_city)
        t1.start()
    
    obj.text.config(text="Kůň", font=("Calibri", 18, "bold"), justify="center")
    obj.l_upgrade1.config(text=f"Doba cesty: \n{obj.stats[(1)]} s", justify="left")
    obj.b_upgrade1.config(text=f"Upgrade (${obj.stats[(2)][1]})", height=2)
    obj.l_upgrade2.config(text=f"Kapacita vozu: \n{obj.stats[(3)]} barelů", justify="left")
    obj.b_upgrade2.config(text=f"Upgrade (${obj.stats[(4)][1]})", height=2)
    obj.b_send.config(text="Prodat ropu!", command=horse_go)
    obj.b_build.config(text="Koupit koně", command=obj.buy)

    
    obj.text.grid(row=0, column=0, columnspan=2)
    obj.b_build.grid(row=1, column=0, columnspan=2) 


def silo(obj:Upgrade) -> None:
    """Sets default values for the "silo" type of upgrade."""
    pass

def rig(obj:Upgrade) -> None:
    """Sets default values for the "rig" type of upgrade."""
    pass

    obj.text.config(text="Těžební věž", font=("Calibri", 18, "bold"), justify="center")
    obj.l_upgrade1.config(text=f"Rychlost těžby: \n {obj.stats[(1)]}x", justify="left")
    obj.b_upgrade1.config(text=f"Upgrade (${obj.stats[(2)][1]})", height=2)
    obj.l_upgrade2.config(text=f"Efektivita: \n +{obj.stats[(3)]} %", justify="left")
    obj.b_upgrade2.config(text=f"Upgrade (${obj.stats[(4)][1]})", height=2)
    obj.b_send.config(text="Postavit věž")
    obj.b_build.config(text="Koupit novou věž", command=obj.buy)

    obj.l_description1.config(text=f"Kvalita pole: {obj.stats[(5)]}")
    obj.l_description2.config(text=f"Aktuální rychlost těžby: {obj.stats[(6)]} bar/den")

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



unitsize = 8
cfg_values = json.load(open("./data/config.json","r", encoding="UTF-8"))
print(cfg_values["sizex"])
# config = {"riglimit" : 5}
# rigs = [0,1]
# riglimit = 5
# okno = Tk()
# x = Tile(okno, (0,0), 1500, 5)
# okno.mainloop()

#Starting variables
money = 2000
seed = 3
mapsize = 10
pos_cache = None
noise = PerlinNoise(3, seed)
mainframe = Tk()
map_frame = Frame(mainframe)
rig_frame = Frame(mainframe)
horse_frame = Frame(mainframe)


emptyim = PhotoImage()
game_end = threading.Event()

oil_fields = [[Tile(map_frame, (x,y), 500, noise([x/mapsize,y/mapsize])) for y in range(mapsize)] for x in range(mapsize)]

# x = Upgrade(y, "horse", 1)
# x2 = Upgrade(y, "horse", 2)
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
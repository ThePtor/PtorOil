# PtorOil
# Zápočtový program
# Pavel Rak
# LS 2022/23

import json
import threading
import time
import copy
import random
import math
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from perlin_noise import PerlinNoise
from matplotlib import pyplot as plt

class Tile:
    """Class for oil tiles on map"""
    def __init__(self, master, position, size) -> None:
    
        self.but = Button(master, font=txt_s, command=self.reveal, width=20*baseunit, height=20*baseunit, image=emptyim, compound='bottom', padx=0, pady=0,)
        self.active = False
        self.pos = position
        self.size = size
        self.qual = self.get_qual()
        self.oil = self.get_oil()
        self.mineable = False
        self.but.grid(row=self.pos[0], column=self.pos[1])
        #self.but.config(bg=rgbtohex(0, 180, min(int(self.qual*150), 255)))
    
    def reveal(self):
        global dowsers
        res = False
        if dowsers > 0:
            dowsers -= 1 
            res = True
        else:
            res = check_money(plot_price)
        if res:
            self.but.config(background="green", text=f"{self.qual:.2f}")
            print(self.oil)
            self.mineable = True
            self.but.config(command=self.tile_pass)
            self.but.config(bg=rgbtohex(0, 180, min(int(self.qual*150), 255)))

    def get_qual(self):
        quality = (1.2+qual_noise((self.pos[0]/self.size[0], self.pos[1]/self.size[1])))
        return quality

    def get_oil(self):
        oil = 4**(2*oil_noise((self.pos[0]/self.size[0], self.pos[1]/self.size[1])))
        oil *= 100
        return oil

    def tile_pass(self):
        global pos_cache
        if pos_cache == self.pos:
            pos_cache = None
            self.but.config(relief=RAISED)
        else:
            if pos_cache:
                oil_fields[pos_cache[0]][pos_cache[1]].but.config(relief=RAISED)
            pos_cache = self.pos
            self.but.config(relief=SUNKEN)
        toggle_rigs()
    
    def close_tile(self, mode=0):
        """mode 0 = rig destroyed
            mode 1 = tile mined"""
        if mode == 0:
            self.but.config(text=f"{self.qual:.2f}\n???")
        elif mode == 1:
            self.but.config(text=f"{self.qual:.2f}\n{self.oil:.0f}")
        self.but.config(bg=rgbtohex(0, 180, int(self.qual*150)))

class Upgrade:
    """Class for upgradable buildings - horse, silo, mining rig."""
    def __init__(self, master, version, number=0) -> None:
        self.box = Frame(master, height=100*baseunit, width=78*baseunit)
        self.box.grid_propagate(False)
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
        self.stats  = {"speed" : {"level": 0, "cap": 4, "val": [15, 10, 6, 4, 3], "price": [0, 1999, 5000, 6900, 12300]}, #speed/mining speed
                       "capacity" : {"level": 0, "cap": 4, "val": [0.5, 1, 2, 500, 56], "price": [250, 500, 1000, 250, 600]}, #capacity/mining effectivity
                       "quality" : 0, #plot quality
                       "oil" : 0, #remaining oil
                       "cur_speed" : 0, #current mining speed
                       }
        self.bar = ttk.Progressbar(self.box)
        self.timer  = 0
        self.upgrades = int
        self.pos = (-1,-1)
        self.available = False
        self.active = False
        self.assign_type(version)
        self.activate()

# General use Upgrade class functions
#        
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
        self.box.grid_columnconfigure(0, weight=2)
        self.box.grid_columnconfigure(1, weight=1)
        # self.box.grid_rowconfigure(0, weight=1)
        # self.box.grid_columnconfigure(0, weight=1)
        
        
    def update_text(self):
        """Intentionally empty placeholder function"""
        pass


    def level_up(self, upgradename):
        global demand
        if check_money(upgradename['price'][upgradename['level']+1]):
            upgradename['level'] += 1
            demand += demand_step
            self.update_text()
            moneycounter.config(text=f"${money:.0f}")

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
            
            if self.version == "silo":
                self.bar.grid(row=3, column=0, columnspan=2)

            if self.version == "rig":
                self.l_description1.grid(row=4, column=0, columnspan=2)
                self.l_description2.grid(row=5, column=0, columnspan=2)
                toggle_rig(self)
    
# Rig functions

    def rig(self) -> None:
        """Sets default values for the "rig" type of upgrade."""
        self.stats = copy.deepcopy(rig_cfg)
        self.names = msg_rig    
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        
        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))
        self.b_send.config(text=f"{self.names['build']}", command=self.build_rig)
        self.b_build.config(text=f"{self.names['buy']}\n(${self.stats['capacity']['price'][0]})", command=self.buy)

        

        def txt_s():
            """Modifies text to fit the rig structure"""
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]:.2f} x", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']['val'][self.stats['capacity']['level']]:.0%}", justify="left")
            self.l_description1.config(text=f"{self.names['quality']} {self.stats['quality']:.2f}")
            self.l_description2.config(text=f"{self.names['cur_speed']} \n{self.stats['cur_speed']:.2f} bar/den")
            if self.stats['speed']['level'] < self.stats['speed']['cap']:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < self.stats['capacity']['cap']:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)


        self.update_text = txt_s
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2)

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
    
    def destroy_rig(self, mode=0):
        self.stats['quality'] = 0
        self.stats['cur_speed'] = 0
        self.update_text()
        self.b_send.config(text=self.names['build'], fg="black", command=self.build_rig)
        
        oil_fields[self.pos[0]][self.pos[1]].close_tile(mode)
        self.pos = (-1, -1)
        self.available = True
        self.active = False
        self.update_text()
        toggle_rig(self)

    def dig_oil(self):
        """Rig function that digs oil"""
        efi = self.stats['capacity']
        spd = self.stats['speed']
        
        mined = self.stats['quality'] * spd['val'][spd['level']] * (1+ (3**oil_noise((self.pos[0]/mapsize, self.pos[1]/mapsize, day/7))))
        # print(mined)
        decrease = mined/efi['val'][efi['level']]
        
        if self.stats['oil'] < decrease:
            
            mined = self.stats['oil'] * efi['val'][efi['level']]
            self.stats['oil'] = 0
            self.destroy_rig(mode=1)
        else:
            self.stats['oil'] -= decrease
        self.stats['cur_speed'] = mined
        return mined

    



# Horse functions

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

        self.stats = copy.deepcopy(horse_cfg)
        self.names = msg_horse
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))
        self.b_send.config(text=self.names['sell_cmd'], command=horse_go)
        self.b_build.config(text=f"{self.names['buy']}\n(${self.stats['capacity']['price'][0]})", command=self.buy)

        def txt_s():
            # self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']} s", justify="left")
            # self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']} barelů", justify="left")
        
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]} {msg_general['day']}", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['capacity']['val'][self.stats['capacity']['level']]} {msg_general['bar']}", justify="left")
            if self.stats['speed']['level'] < self.stats['speed']['cap']:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < self.stats['capacity']['cap']:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)

        self.update_text = txt_s
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2)

    def goto_city(self):
        """does one step towards city to sell oil"""
        self.timer -= 1
        if self.timer <= 0:
            self.kill_horse()
        elif self.timer <= (self.stats['speed']['val'][self.stats['speed']['level']]/3):
            self.b_send.config(text=f"{self.names['back']} ({self.timer} {msg_general['day']})")
        elif self.timer <= (self.stats['speed']['val'][self.stats['speed']['level']]/3 + 1):
            self.b_send.config(text=f"+${self.sell_oil():.2f}")
        else:
            self.b_send.config(text=f"{self.names['forward']} ({self.timer} dní)")
        #UNFINISHED
        # print(self.timer)
    
    def kill_horse(self):
        self.active = False        
        self.b_send.config(text=self.names['sell_cmd'], state=ACTIVE)
        # UNFINISHED

    def sell_oil(self):
        """Horse function that sells oil."""
        global money, soldoil
        profit = self.stats['oil'] * price
        soldoil += self.stats['oil']
        self.stats['oil'] = 0
        money += profit
        moneycounter.config(text=f"${money:.0f}")
        return profit

# Silo functions

    def silo(self) -> None:
        """Sets default values for the "silo" type of upgrade."""
        self.names = msg_silo    
        self.text.config(text=self.names['name'], font=("Calibri", 18, "bold"), justify="center")
        self.stats = copy.deepcopy(silo_cfg)
        self.bar.config()

        self.b_upgrade1.config(height=2, command=lambda: self.level_up(self.stats['speed']))
        self.b_upgrade2.config(height=2, command=lambda: self.level_up(self.stats['capacity']))

        

        def txt_s():
            self.l_upgrade1.config(text=f"{self.names['speed']} \n{self.stats['speed']['val'][self.stats['speed']['level']]:.2f} {msg_general['day']}", justify="left")
            self.l_upgrade2.config(text=f"{self.names['capacity']} \n{self.stats['oil']:.2f}/{self.stats['capacity']['val'][self.stats['capacity']['level']]} bar", justify="left")

            self.bar.config(value=self.stats['oil'], maximum=self.stats['capacity']['val'][self.stats['capacity']['level']])    

            if self.stats['speed']['level'] < self.stats['speed']['cap']:
                self.b_upgrade1.config(text=f"{self.names['upgrade']} \n(${self.stats['speed']['price'][self.stats['speed']['level']+1]})")
            else:
                self.b_upgrade1.config(text=f"{self.names['max_level']}", state=DISABLED)
            if self.stats['capacity']['level'] < self.stats['capacity']['cap']:
                self.b_upgrade2.config(text=f"{self.names['upgrade']} \n(${self.stats['capacity']['price'][self.stats['capacity']['level']+1]})")
            else:
                self.b_upgrade2.config(text=f"{self.names['max_level']}", state=DISABLED)


        self.update_text = txt_s
        self.update_text()
        self.text.grid(row=0, column=0, columnspan=2)
        self.b_build.grid(row=1, column=0, columnspan=2)

    def add_oil(self, amt):
        """Method of adding oil into oilsilo"""
        self.stats['oil'] += amt
        if self.stats['oil'] > self.stats['capacity']['val'][self.stats['capacity']['level']]:
            over = self.stats['oil'] - self.stats['capacity']['val'][self.stats['capacity']['level']]
            self.stats['oil'] = self.stats['capacity']['val'][self.stats['capacity']['level']]
            fine = self.spillage(over)
        else:
            self.timer = max(self.timer-1, 0)
            if self.timer == 0:
                self.stats['cur_speed'] /= 2
            fine = 0
        return fine

    def spillage(self, amt):
        """Silo function that fines player if silo overflows."""
        self.stats['cur_speed'] += amt
        self.timer += 1
        fine = 0
        if self.timer > self.stats['speed']['val'][self.stats['speed']['level']]:
            self.timer -= 1
            fine = self.stats['cur_speed']/2
            self.stats['cur_speed'] /= 2
            print(f"Spillage {fine:.2f}")
        return fine

def rgbtohex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}"

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

#Game round functions    
def correct_price():
    global soldoil, oilbuffer, oiltimer
    if soldoil != 0:
        oiltimer += 1
    drop = min(soldoil, 2**(oiltimer/2))
    rise = 0
    soldoil -= drop
    oilbuffer += drop
    cor = oilbuffer * pricedrop
    if oiltimer > 4:    
        rise = min(oilbuffer, (oiltimer)**(0.5+demand))
        oilbuffer -= rise
    # print(f"Drop in price {drop:.2f}, Rise in price {rise:.2f}, {soldoil:.2f}, {oilbuffer:.2f}")
    if (soldoil == 0) and (oilbuffer == 0):
        oiltimer = 0
    r_price = qual_noise((-1,-1, 3*day/yearlen))
    price = 50 + (100*r_price - cor)
    if price < 0:
        price = abs(1 / price)

    return price

def update_price():
    global pricedelta, price
    price = correct_price()
    pricelog.append(price)
    cur_price.config(text=f"${price:.2f}/bar")

def get_date():
    date = day%365
    date += 1
    res = ""
    if date <= 31:
        res = f"{date-0}. {msg_general['jan']}"
    elif date <= 59:
        res = f"{date-31}. {msg_general['feb']}"
    elif date <= 90:
        res = f"{date-59}. {msg_general['mar']}"
    elif date <= 120:
        res = f"{date-90}. {msg_general['apr']}"
    elif date <= 151:
        res = f"{date-120}. {msg_general['may']}"
    elif date <= 181:
        res = f"{date-151}. {msg_general['jun']}"
    elif date <= 212:
        res = f"{date-181}. {msg_general['jul']}"
    elif date <= 243:
        res = f"{date-212}. {msg_general['aug']}"
    elif date <= 273:
        res = f"{date-243}. {msg_general['sep']}"
    elif date <= 304:
        res = f"{date-273}. {msg_general['oct']}"
    elif date <= 334:
        res = f"{date-304}. {msg_general['nov']}"
    else:
        res = f"{date-334}. {msg_general['dec']}"
    return res

def gametick():
    global day, dowsers
    day += 1
    if (day % dowserdelay) == 0:
        dowsers += 1
    cur_date.config(text=get_date())
    if day > yearlen:
        end_game()
    dug_oil = 0
    for rig in rig_field:
        if rig.active:
            dug_oil += rig.dig_oil()
            rig.update_text()
    spill_fine = oil_silo.add_oil(dug_oil)
    # oil_silo.stats['oil'] += 10
    oil_silo.update_text()
    for hrs in herd:
        if hrs.active:
            hrs.goto_city()
    update_price()

    time.sleep(1/gamespeed)
    
def timer():
    while not game_end.is_set():
        gametick()

#File handling functions
def load_configs():
    """Loads settings from config files, if an error occurs, uses default configs"""
    try:
        with open("./data/horse.json") as file:
            horse_tmp = json.load(file)
            for x in horse_cfg:
                try:
                    horse_cfg[x] = horse_tmp[x]
                except KeyError:
                    pass
                    
    except FileNotFoundError:
        pass

    try:
        with open("./data/rig.json") as file:
            rig_tmp = json.load(file)
            for x in rig_cfg:
                try:
                    rig_cfg[x] = rig_tmp[x]
                except KeyError:
                    pass
                    
    except FileNotFoundError:
        pass

    try:
        with open("./data/silo.json") as file:
            silo_tmp = json.load(file)
            for x in silo_cfg:
                try:
                    silo_cfg[x] = silo_tmp[x]
                except KeyError:
                    pass
                    
    except FileNotFoundError:
        pass

def start_menu(master):
    mainim = Label(master, text="PtorOil", font=txt_s, image=emptyim, compound="bottom", height=baseunit*50, width=baseunit*120)
    start_game = Button(master, text="Quick Game", command=game_launch)
    quit_game = Button(master, text="Quit", command=mainframe.destroy)
    mainim.pack()
    start_game.pack()
    quit_game.pack()
    

def game_launch():
    menu.grid_remove()
    gameframe.grid()

    t1 = threading.Thread(target=timer)
    t1.start()


def end_game():
    global money
    print(day)
    game_end.set()
    gameframe.grid_remove()
    endsell = 0
    for horse in herd:
        if horse.timer > 0:
            endsell += horse.stats['oil']
    money += (endsell*price)
    log['money'] = money
    endnotice = Label(endscreen, text="Konec hry!")
    results = Label(endscreen, text=f"Skóre: {log['money']- log['loan']:.0f}")
    endscreen.grid_rowconfigure(0, weight=3)
    endscreen.grid_rowconfigure(1, weight=1)
    endnotice.grid(row=0)
    results.grid(row=1)
    endscreen.grid()
    


# Dimensions functions
def gamewindow_grid(frm:Frame):
    frm.grid_columnconfigure(0, weight=6)
    frm.grid_columnconfigure(1, weight=3)
    frm.grid_columnconfigure(2, weight=7)
    frm.grid_rowconfigure(0, weight=1)
    frm.grid_rowconfigure(1, weight=2)
    frm.grid_rowconfigure(2, weight=3)
    frm.grid_rowconfigure(3, weight=3)

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

horse_cfg = {"speed" : {"level": 0, "cap": 4, "val": [15, 10, 6, 4, 3], "price": [0, 1999, 5000, 6900, 12300]}, #speed/mining speed
            "capacity" : {"level": 0, "cap": 4, "val": [10, 15, 25, 40, 60], "price": [250, 500, 1000, 250, 600]}, #capacity/mining effectivity
            "quality" : 0, #plot quality
            "oil" : 0, #remaining oil
            "cur_speed" : 0, #current mining speed
            }

rig_cfg = {"speed" : {"level": 0, "cap": 4, "val": [15, 10, 6, 4, 3], "price": [0, 1999, 5000, 6900, 12300]}, #speed/mining speed
            "capacity" : {"level": 0, "cap": 4, "val": [0.5, 1, 2, 500, 56], "price": [250, 500, 1000, 250, 600]}, #capacity/mining effectivity
            "quality" : 0, #plot quality
            "oil" : 0, #remaining oil
            "cur_speed" : 0, #current mining speed
            } 

silo_cfg = {"speed" : {"level": 0, "cap": 4, "val": [15, 10, 6, 4, 3], "price": [0, 1999, 5000, 6900, 12300]}, #speed/mining speed
            "capacity" : {"level": 0, "cap": 4, "val": [0.5, 1, 2, 500, 56], "price": [250, 500, 1000, 250, 600]}, #capacity/mining effectivity
            "quality" : 0, #plot quality
            "oil" : 0, #remaining oil
            "cur_speed" : 0, #current mining speed
            } 


with open("./data/config.json","r", encoding="UTF-8") as cfg_data:
    cfg_values = json.load(cfg_data)
print(cfg_values["sizex"])
# config = {"riglimit" : 5}
# rigs = [0,1]
# riglimit = 5
# okno = Tk()
# x = Tile(okno, (0,0), 1500, 5)
# okno.mainloop()

baseunit = 2
#Default variables
money = 2500 #starting money
dowsers = 3 #starting dowsers
dowserdelay = 15 #delay between free dowsers
plot_price = 1000 #reveal price without dowser
day = 0 #current day
pricedelta = 0 
price = 0 #corrent oil price
oilbuffer = 0 #oil lowering the price
oiltimer = 0 
soldoil = 0 #sold oil buffer
seed = 3 
spillage_severity = 1 #spillage fine severity
demand = 0 #speed of price recovery after 
demand_step = 0.01 #effect of upgrade on price recovery
pricedrop = 0.3 #how much sold barrel affects price
pricelog = []
# Log variables

log = {'oilbuffer' : 0,
       'total_mined' : 0,
       'total_sold' : 0,
       'spillage_fine' : 0,
       'loan' : 0,
       'money' : 0,
       }

gamespeed = 10
mainframe = Tk()
mainframe.geometry(f"{baseunit*640}x{baseunit*360}")
gameframe = Frame(mainframe, width=baseunit*640, height=baseunit*360,)# bg="green")
# gameframe.grid_propagate(0)
menu = Frame(mainframe)
setup = Frame(mainframe)
endscreen = Frame(mainframe)
emptyim = PhotoImage()

txt_s = font.Font(family="TkDefaultFont", size=4+baseunit*4)
txt_m = font.Font(family="Algerian")
txt_l = font.Font(family="TkDefaultFont")


# gameframe layout
date_frame = Frame(gameframe, width=240*baseunit, height=40*baseunit)
bank_frame = Frame(gameframe, width=240*baseunit, height=80*baseunit)
map_frame = Frame(gameframe, height=240*baseunit, width=240*baseunit)
rig_frame = Frame(gameframe, width=400*baseunit, height=120*baseunit)#, bg="yellow")
horse_frame = Frame(gameframe, width=400*baseunit, height=120*baseunit)#, bg="red")
silo_frame = Frame(gameframe, width=120*baseunit, height=120*baseunit)#, bg="blue")


game_end = threading.Event()
# gamewindow_grid(gameframe)
date_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=NSEW)
bank_frame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=N)
map_frame.grid(row=2, column=0, rowspan=2, columnspan=1, sticky=N)
silo_frame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky=N)
horse_frame.grid(row=2, column=1, rowspan=1, columnspan=2, sticky=N)
rig_frame.grid(row=3, column=1, rowspan=1, columnspan=2, sticky=N)

gameframe.grid_propagate(False)
date_frame.grid_propagate(False)
bank_frame.grid_propagate(False)
map_frame.grid_propagate(False)
horse_frame.grid_propagate(False)
rig_frame.grid_propagate(False)

date_frame.grid_columnconfigure(0, weight=1)
date_frame.grid_rowconfigure(0, weight=1)
bank_frame.grid_columnconfigure(0, weight=3)
bank_frame.grid_rowconfigure(0, weight=1)
bank_frame.grid_columnconfigure(1, weight=1)
for x in range(5):
    rig_frame.grid_columnconfigure(x, weight=1)
    horse_frame.grid_columnconfigure(x, weight=1)
# Labels
moneycounter = Label(bank_frame, text=f"${money:.0f}", font=("Algerian", 35))
cur_price = Label(date_frame, text=f"${price:.2f}/bar", font=("CMU Serif", 24), padx=baseunit*5)
cur_date = Label(date_frame, text=get_date(), font=("CMU Serif", 24), padx=baseunit*5)
moneycounter.grid()
cur_price.grid(row=0, column=0, sticky=W)
cur_date.grid(row=0, column=1, sticky=E)

yearlen = 365

#Startup variables






levelcap = 2
seed = random.random()
mapsize = 10
pos_cache = None
qual_noise = PerlinNoise(4, seed)
oil_noise = PerlinNoise(2, 2*seed)
# noise = PerlinNoise(4, random.random())


load_configs()

oil_fields = [[Tile(map_frame, (x,y), (mapsize, mapsize)) for y in range(mapsize)] for x in range(mapsize)]

# x = Upgrade(y, "horse", 1)
# x2 = Upgrade(y, "horse", 2)





oil_silo = Upgrade(silo_frame, "silo")
oil_silo.buy(True)
herd = [Upgrade(horse_frame, "horse", x) for x in range(5)]
herd[0].buy(True)
rig_field = [Upgrade(rig_frame, "rig", x) for x in range(5)]
rig_field[0].buy(True)

update_price()
start_menu(menu)
menu.grid()
# gameframe.grid()
mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_rowconfigure(0, weight=1)
mainframe.mainloop()

game_end.set()
print("69")
leng = mapsize
# vallist = [[4**(2*oil_noise((x/leng, y/leng))) for y in range(leng)] for x in range(leng)]
# print(sum(vallist)/len(vallist))
# plt.imshow(vallist, cmap='gray')
# plt.show()
# vallist = [[1*(1.2+qual_noise((x/leng, y/leng))) for y in range(leng)] for x in range(leng)]
# plt.imshow(vallist, cmap='gray')
# plt.show()
plt.plot(pricelog)
plt.show()

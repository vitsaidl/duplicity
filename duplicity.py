# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 09:21:36 2018

@author: Vit Saidl
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os


def nahrajSoubor(*args):
    jmenoNactenehoSouboru =filedialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)) ,title = "Výběr souboru", filetypes = (("csv soubory","*.csv"),("txt soubory","*.txt"), ("Všechny soubory","*.*")))
    hodnotaHlavickyCombobox = comboboxHlavicka.get()    #nacteni informace o tom, kde je hlavicka souboru
    separator = comboboxSeparator.get()                 #nacteni separatoru oddelujiciho sloupce
    global nactenaTabulka                               #nactenaTabulka je globalni promenna, tj. jeji zmeny v teto funkci se projevi i vne funkce
    
    if(jmenoNactenehoSouboru != ""):                    #prazdny nazev nstane napriklad pri zmacknuti cancelu
        global sloupceNaPridani
        
        if (separator == "mezera"): separator = "\s"         #mapping nazvu specialnich separatoru z combobosu na realny separator
        elif (separator == "tabulátor"): separator = "\t"
        
        jmenaSloupcu = None                                  #defaultne je list jmen sloupcu neexistujici (tj. neprepise hlavicku realne existujici v souboru)
        if (hodnotaHlavickyCombobox == "Není (momentalne nepodporovane)"): hlavickaNastaveni = None             #na zaklade hodnoty vybrane v comboboxu se nastavuje, kde (ne)ma hlavicka hledat
        elif (hodnotaHlavickyCombobox == "Na prvním řádku"): hlavickaNastaveni = 0   #0 realne znamena prvni radek souboru
        elif (hodnotaHlavickyCombobox == "Zadá se ručně"):
            hlavickaNastaveni = 0                                     #tj. mame tu hodnotu ruznou od None, tj. hlavicka existuje, ale je z nejakeho duvodu spatna
            stringJmenSloupcu = oblastRucniHlavicka.get("1.0",tk.END) #nacitame z textoveho pole; "1.0" znamena, ze cteme od prvniho radku, znaku nula (= prvni znak); END znamena, ze cteme az do konce text boxu
            jmenaSloupcu = stringJmenSloupcu.split(",")               #string rozdelime podle carky a vlozime do listu
            jmenaSloupcu = list(map(str.strip,jmenaSloupcu))          #z okraju kusu stringu usekneme bile znaky (map fce uplatnuje split individualne na kazdy prvek listu)
        
        nactenaTabulka = pd.read_csv(jmenoNactenehoSouboru, names = jmenaSloupcu, header = hlavickaNastaveni, sep = separator)  #nyni dochazi k nacteni souboru
        report = "Počet řádků tabulky je {}\n".format(len(nactenaTabulka))    #vytvareji se promenne pro report
        for sloupec in nactenaTabulka.columns:
            report = report + "Počet unikátních hodnot sloupce {}: {}\n".format(sloupec, (nactenaTabulka[sloupec]).nunique())
        oblastShrnuti.config(state=tk.NORMAL)                                #textove pole por report se otevre pro upravy
        oblastShrnuti.insert(tk.END, report)                                 #upravy se vlozi na konec v poli aktualne pritomneho textu
        oblastShrnuti.config(state=tk.DISABLED)                              #a textove pole se zavre pro upravy
        
        sloupceNaPridani = list(nactenaTabulka.columns)                      #vezmou se nazvy sloupecku z pandiho datasetu
        comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani         #a vlozi se do seznamu adeptu na kontrolu duplicit
    
    else:
        messagebox.showerror("Error", "Nebyl vybrán soubor")                 #pokud nebyl vybran soubor, tak s tim uzivatele otravujeme
       
def pridejSloupec(*args):   #funkce pridavajici sloupec do seznamu, na zaklade ktereho se posleze urci duplicity
    global sloupceNaPridani                                                  #nastaveni promennych jako globalni
    global sloupceNaDuplicitu
    global sloupceNaOdebrani
    jmenoSloupce = comboboxPridaniKontrolaDuplicit.get()                     #vezme se aktualne vybrana polozka v comboboxu pridavajici sloupec
    sloupceNaPridani.remove(jmenoSloupce)                                    #a odebere se z listu sloupceNaPridani
    sloupceNaDuplicitu.append(jmenoSloupce)                                  #aby se pridala do dalsich dvou listu
    sloupceNaOdebrani.append(jmenoSloupce) 
    comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani             #comboboxy se nasledne preplni odpovidajicimi listy
    comboboxSeznamSloupcuDuplicity["values"] = sloupceNaDuplicitu
    comboboxOdebraniKontrolaDuplicit["values"] = sloupceNaOdebrani
    
def odeberSloupec(*args): #funkce odebirajici sloupec ze seznamu, na zaklade ktereho se posleze urci duplicity
    global sloupceNaPridani                                                  #nastaveni promennych jako globalni
    global sloupceNaDuplicitu
    global sloupceNaOdebrani
    jmenoSloupce = comboboxOdebraniKontrolaDuplicit.get()                    #vezme se aktualne vybrana polozka v comboboxu odebirajicim sloupec
    sloupceNaPridani.append(jmenoSloupce)                                    #prida se do listu sloupceNaPridani,
    sloupceNaDuplicitu.remove(jmenoSloupce)                                  #aby se odebrala z dvou dalsich listu
    sloupceNaOdebrani.remove(jmenoSloupce)
    comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani             #comboboxy se nasledne preplni odpovidajicimi listy
    comboboxSeznamSloupcuDuplicity["values"] = sloupceNaDuplicitu
    comboboxOdebraniKontrolaDuplicit["values"] = sloupceNaOdebrani
    
def vygenerujVysledek(*args):
    global nactenaTabulka                                                    #nastaveni promennych jako globalnich
    global sloupceNaDuplicitu
    global coJeDuplicita
    if (coJeDuplicita.get() == 1):                                           #na zaklade radiobuttonu nastavime, co minime duplicitou
        duplicitaFlag = "first"                                              #jestli prvni vyskyt radku, ktery ma dale v souboru svuj klon, se za duplicitu nepovazuje
    else:
        duplicitaFlag = False                                                #nebo povazuje
    listBooleanu = nactenaTabulka.duplicated(subset =sloupceNaDuplicitu, keep = duplicitaFlag )  #vytvori se list, jehoz kazdy prvek odpovida jednomu radku tabulky, a ktery obsahuje True/False (true je pro duplikaty)
    if(coChceme.get() == 1):                                                 #pokud nechceme duplikaty, ale unikatni hodnoty
        listBooleanu = [not x for x in listBooleanu]                         #tak musime ze vsech true udelat false a naopak
    
    vysledek = nactenaTabulka[listBooleanu]                                  #nakonec z datasetu vybereme radky, ktere jsou podle listu booleanu true
    vysledek.to_csv(os.path.dirname(os.path.realpath(__file__)) + "\\vysledek_hledani.csv", sep = comboboxSeparator.get())  #a ulozime soubor s nimi do stejneho adresare, jako je tento program

#globalni promenne (nevim totiz, jak je rozumne dostat z okenich funkci)
sloupceNaPridani = []
sloupceNaDuplicitu = []
sloupceNaOdebrani = []
nactenaTabulka = ""

root = tk.Tk()
root.title("Hledání duplicit v extraktu")
mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


labelSeparator = ttk.Label(mainframe, text= "Volba separátoru sloupců")
labelSeparator.grid(column=0, row=0, sticky =tk.W)
comboboxSeparator = ttk.Combobox(mainframe, values = [",", ".", ";", ":", "|", "/", "\\", "mezera", "tabulátor"], state= "readonly")
comboboxSeparator.grid(column=0, row=0, sticky =tk.E)
comboboxSeparator.set(",")

labelHlavicka = ttk.Label(mainframe, text= "Hlavička")
labelHlavicka.grid(column=0, row=1, sticky =tk.W)
comboboxHlavicka = ttk.Combobox(mainframe, values = ["Není (momentalne nepodporovane)", "Na prvním řádku", "Zadá se ručně"])
comboboxHlavicka.grid(column=0, row=1, sticky =tk.E)
comboboxHlavicka.set("Na prvním řádku")

labelRucniHlavicka = ttk.Label(mainframe, text= "Custom hlavička - názvy sloupců oddělujte čárkou")
labelRucniHlavicka.grid(column=0, row=2)
oblastRucniHlavicka = tk.Text(mainframe, height = 1, width = 80)     #tato sirka realne urcuje sirku okna
oblastRucniHlavicka.grid(column=0, row=3)

tlacitkoNahrajSoubor = ttk.Button(mainframe, text= "Nahrání souboru", command = nahrajSoubor)
tlacitkoNahrajSoubor.grid(column=0, row=4)

labelOblastiShrnuti = ttk.Label(mainframe, text = "Shrnutí")
labelOblastiShrnuti.grid(column = 0, row = 5)
oblastShrnuti = tk.Text(mainframe, height = 8, width = 80)
oblastShrnuti.config(state=tk.DISABLED)
oblastShrnuti.grid(column = 0, row = 6, sticky =tk.W)

labelPridaniKontrolaDuplicit = ttk.Label(mainframe, text = "Přidat do seznamu")
labelPridaniKontrolaDuplicit.grid(column = 0, row = 7, sticky =tk.W)
comboboxPridaniKontrolaDuplicit = ttk.Combobox(mainframe)
comboboxPridaniKontrolaDuplicit.grid(column=0, row=8, sticky =tk.W)
tlacitkoPridejSloupec = ttk.Button(mainframe, text= "Přidej sloupec", command = pridejSloupec)
tlacitkoPridejSloupec.grid(column=0, row=9, sticky =tk.W)

labelSeznamSloupcuDuplicity = ttk.Label(mainframe, text = "Sloupce tvořících subtabulku zkoumanou kvůli duplicitám")
labelSeznamSloupcuDuplicity.grid(column = 0, row = 7)
comboboxSeznamSloupcuDuplicity  = ttk.Combobox(mainframe)
comboboxSeznamSloupcuDuplicity.grid(column=0, row=8)

labelOdebraniKontrolaDuplicit = ttk.Label(mainframe, text = "Odebrat ze seznamu")
labelOdebraniKontrolaDuplicit.grid(column = 0, row = 7, sticky =tk.E)
comboboxOdebraniKontrolaDuplicit = ttk.Combobox(mainframe)
comboboxOdebraniKontrolaDuplicit.grid(column=0, row=8, sticky =tk.E)
tlacitkoOdeberSloupec = ttk.Button(mainframe, text= "Odeber sloupec", command = odeberSloupec)
tlacitkoOdeberSloupec.grid(column=0, row=9, sticky =tk.E)

labelCoPatriDoDuplicity = ttk.Label(mainframe, text = "Duplicitou míníme")
labelCoPatriDoDuplicity.grid(column = 0, row = 10)
coJeDuplicita = tk.IntVar()    #specialni tkinterovska promenna svazujici dva radiobuttony
radiobuttonCoPatriDoDuplicity = ttk.Radiobutton(mainframe, text = "Druhý a další výskyty určité hodnoty", variable = coJeDuplicita, value = 1)
radiobuttonCoPatriDoDuplicity.grid(column=0, row=11)
radiobuttonCoPatriDoDuplicity = ttk.Radiobutton(mainframe, text = "Všechny výskyty určité hodnoty (včetně prvního)", variable = coJeDuplicita, value = 2)
radiobuttonCoPatriDoDuplicity.grid(column=0, row=12)

labelCoChceme = ttk.Label(mainframe, text = "Chceme")
labelCoChceme.grid(column = 0, row = 13)
coChceme = tk.IntVar()
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Unikátní řádky", variable = coChceme, value = 1)
radiobuttonCoChceme.grid(column=0, row=14)
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Duplicitní řádky", variable = coChceme, value = 2)
radiobuttonCoChceme.grid(column=0, row=15)

tlacitkoVygenerujVysledek = ttk.Button(mainframe, text= "Vygeneruj výsledný soubor", command = vygenerujVysledek)
tlacitkoVygenerujVysledek.grid(column=0, row=16)

root.mainloop()  




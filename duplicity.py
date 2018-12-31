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
    hodnotaKodovaniComboboxu = comboboxKodovani.get()   #nacteni informace o pouzitem kodovani zkoumaneho souboru
    separator = comboboxSeparator.get()                 #nacteni separatoru oddelujiciho sloupce
    global nactenaTabulka                               #nactenaTabulka je globalni promenna, tj. jeji zmeny v teto funkci se projevi i vne funkce
    
    if(jmenoNactenehoSouboru != ""):                    #prazdny nazev nastane napriklad pri zmacknuti cancelu
        global sloupceNaPridani
        global sloupceNaDuplicitu
        global sloupceNaOdebrani 
        global nactenaTabulka
                
        #sekce na vyciteni vlivu nacteni predchoziho souboru
        tlacitkoOdeberSloupec.config(state = tk.DISABLED)                     #disabluji se tlacitka, ktera pred pridanim sloupcu do analyzi nemaji fungovat
        tlacitkoVygenerujVysledek.config(state = tk.DISABLED)
        sloupceNaPridani = []                                                 #vyciti se listy
        sloupceNaDuplicitu = []
        sloupceNaOdebrani = []
        nactenaTabulka = ""                                                  #smaze se pandi dataset
        comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani         #promazou se comboboxy nactenim prazdnych listu
        listboxSeznamSloupcuDuplicity.delete(0, tk.END)                      #promazani listboxu
        listboxSeznamSloupcuDuplicity.insert(tk.END, *sloupceNaDuplicitu)    #a nacteni prvku z listu, prvni parametr rika, odkud se zacina, druhy je typu *args
        comboboxOdebraniKontrolaDuplicit["values"] = sloupceNaOdebrani
        oblastShrnuti.config(state=tk.NORMAL)                                #textove pole por report se otevre pro upravy
        oblastShrnuti.delete("1.0", tk.END)                                  #a nasledne se jeho obsah od zacatku (1.0) do konce (tk.END) vymaze
        oblastShrnuti.config(state=tk.DISABLED)                              #a textove pole se zavre pro upravy
        comboboxOdebraniKontrolaDuplicit.set("")                             #vymazani aktivniho stringu prislusejiciho k predchozimu nactenemu souboru v comboboxu na odebirani sloupcu
        
        if (separator == "mezera"): separator = "\s+"         #mapping nazvu specialnich separatoru z combobosu na realny separator
        elif (separator == "tabulátor"): separator = "\t"
        
        jmenaSloupcu = None                                  #defaultne je list jmen sloupcu neexistujici (tj. neprepise hlavicku realne existujici v souboru)
        flagBezHlavicky = False
        if (hodnotaHlavickyCombobox == "Není"): 
            hlavickaNastaveni = None             #na zaklade hodnoty vybrane v comboboxu se nastavuje, kde (ne)ma hlavicka hledat
            flagBezHlavicky = True               #a nastavi se boolean, ze hlavicku opravud nemame
        elif (hodnotaHlavickyCombobox == "Na prvním řádku"): hlavickaNastaveni = 0   #0 realne znamena prvni radek souboru
        elif (hodnotaHlavickyCombobox == "Zadá se ručně"):
            hlavickaNastaveni = 0                                     #tj. mame tu hodnotu ruznou od None, tj. hlavicka existuje, ale je z nejakeho duvodu spatna
            stringJmenSloupcu = oblastRucniHlavicka.get("1.0",tk.END) #nacitame z textoveho pole; "1.0" znamena, ze cteme od prvniho radku, znaku nula (= prvni znak); END znamena, ze cteme az do konce text boxu
            jmenaSloupcu = stringJmenSloupcu.split(",")               #string rozdelime podle carky a vlozime do listu
            jmenaSloupcu = list(map(str.strip,jmenaSloupcu))          #z okraju kusu stringu usekneme bile znaky (map fce uplatnuje split individualne na kazdy prvek listu)
        
        nactenaTabulka = pd.read_csv(jmenoNactenehoSouboru, names = jmenaSloupcu, header = hlavickaNastaveni, sep = separator, encoding = hodnotaKodovaniComboboxu)  #nyni dochazi k nacteni souboru
        report = "Počet řádků tabulky je {}\n".format(len(nactenaTabulka))    #vytvareji se promenne pro report
        for sloupec in nactenaTabulka.columns:
            report = report + "Počet unikátních hodnot sloupce {}: {}\n".format(sloupec, (nactenaTabulka[sloupec]).nunique())
        oblastShrnuti.config(state=tk.NORMAL)                                #textove pole por report se otevre pro upravy
        oblastShrnuti.insert(tk.END, report)                                 #upravy se vlozi na konec v poli aktualne pritomneho textu
        oblastShrnuti.config(state=tk.DISABLED)                              #a textove pole se zavre pro upravy
        
        if(flagBezHlavicky == True):                                         #pokud nemame hlavicku, tj. pokud ma nactena tabulka jako jmena sloupcu poradova cisla (a tedy jejich typ je integer)
            nactenaTabulka.columns = list(map(str, nactenaTabulka.columns))  #preevedeme nazvy sloupcu na typ string (v comboboxu by se totiz automaticky prevedly na string a to by delalo neplechu)
                
        sloupceNaPridani = list(nactenaTabulka.columns)                      #vezmou se nazvy sloupecku z pandiho datasetu

        comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani         #a vlozi se do seznamu adeptu na kontrolu duplicit
        if(len(sloupceNaPridani) > 0):                                       #pokud je v listu aspon jeden prvek
            comboboxPridaniKontrolaDuplicit.current(0)                       #nastav aktualni hodnotu comboboxu na nej
    
        tlacitkoPridejSloupec.config(state = tk.NORMAL)                      #odblokovani tlačítka pridavajici sloupce do analyzi opravdu se to nedela pomoci ENABLED, ale pomoci NORMAL
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
    listboxSeznamSloupcuDuplicity.delete(0, tk.END)                          #promazani listboxu
    listboxSeznamSloupcuDuplicity.insert(tk.END, *sloupceNaDuplicitu)        #a nacteni prvku z listu, prvni parametr rika, odkud se zacina, druhy je typu *args
    comboboxOdebraniKontrolaDuplicit["values"] = sloupceNaOdebrani
    
    tlacitkoOdeberSloupec.config(state = tk.NORMAL)                          #enabluj tlacitka na odebirani sloupcu 
    tlacitkoVygenerujVysledek.config(state = tk.NORMAL)                      #a vygenerovani vysledku
    comboboxOdebraniKontrolaDuplicit.current(0)                              #nastav combobox se sloupci k odebrani na neprazdnou hodnotu
    
    if(len(sloupceNaPridani) > 0):                                           #pokud je v listu aspon jeden prvek
        comboboxPridaniKontrolaDuplicit.current(0)                           #nastav aktualni hodnotu comboboxu na nej
    else:
        comboboxPridaniKontrolaDuplicit.set("")                              #jinak nastav combobox na prazdno
        tlacitkoPridejSloupec.config(state = tk.DISABLED)                    #a disabluj tlacitko pridavajici sloupce
    
def odeberSloupec(*args): #funkce odebirajici sloupec ze seznamu, na zaklade ktereho se posleze urci duplicity
    global sloupceNaPridani                                                  #nastaveni promennych jako globalni
    global sloupceNaDuplicitu
    global sloupceNaOdebrani
    jmenoSloupce = comboboxOdebraniKontrolaDuplicit.get()                    #vezme se aktualne vybrana polozka v comboboxu odebirajicim sloupec
    sloupceNaPridani.append(jmenoSloupce)                                    #prida se do listu sloupceNaPridani,
    sloupceNaDuplicitu.remove(jmenoSloupce)                                  #aby se odebrala z dvou dalsich listu
    sloupceNaOdebrani.remove(jmenoSloupce)
    comboboxPridaniKontrolaDuplicit["values"] = sloupceNaPridani             #comboboxy se nasledne preplni odpovidajicimi listy
    listboxSeznamSloupcuDuplicity.delete(0, tk.END)                          #promazani listboxu
    listboxSeznamSloupcuDuplicity.insert(tk.END, *sloupceNaDuplicitu)        #a nacteni prvku z listu, prvni parametr rika, odkud se zacina, druhy je typu *args
    comboboxOdebraniKontrolaDuplicit["values"] = sloupceNaOdebrani
    
    tlacitkoPridejSloupec.config(state = tk.NORMAL)                          #enabluj tlacitko na pridani sloupcu 
    comboboxPridaniKontrolaDuplicit.current(0)                               #nastav combobox se sloupci k pridani na neprazdnou hodnotu
     
    if(len(sloupceNaOdebrani) > 0):                                          #pokud je v listu aspon jeden prvek
        comboboxOdebraniKontrolaDuplicit.current(0)                          #nastav aktualni hodnotu comboboxu na nej
    else:
        comboboxOdebraniKontrolaDuplicit.set("")                             #jinak nastav combobox na prazdno
        tlacitkoOdeberSloupec.config(state = tk.DISABLED)                    #a disabluj tlacitko odebirajici sloupce
        tlacitkoVygenerujVysledek.config(state = tk.DISABLED)                #a tlacitko generujici vysledek
    
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
    vysledek.rename(index = lambda x: x+1, inplace = True)                   #z indexu (ktere zacinaji nulou) delame cisla radku (ktere zacinaji jednickou)
    if(coChceme2.get() == 2): vysledek = vysledek[sloupceNaDuplicitu]        #pokud uzivatel zatrhl, ze chce mit ve vysledku jen sloupce pouzite pri urceni duplicit
    separatorCombobox = comboboxSeparator.get()                              #vezmeme hodnotu separatoru z comboboxu
    if (separatorCombobox == "mezera"): separatorVystup = " "                #mapping nazvu specialnich separatoru z combobosu na realny separator - zde obycejnou mezeru
    elif (separatorCombobox == "tabulátor"): separatorVystup = "\t"          #a zde na tabulator
    else: separatorVystup = separatorCombobox
    jmenoVystupnihoSouboru = os.path.dirname(os.path.realpath(__file__)) + "\\vysledek_hledani.csv"
    pouzitIndex = True                                                       #defaultni hodnota ukazovani cisla radku (resp. indexu; zde je to to same)
    if(checkBoxIndex.state() != ('selected',)):  pouzitIndex = False         #pokud neni zatrzen checkbox, nebude se ukladat index radku 
    vysledek.to_csv(jmenoVystupnihoSouboru, sep =separatorVystup, encoding = comboboxKodovani.get(), index = pouzitIndex)  #a ulozime soubor s nimi do stejneho adresare, jako je tento program
    messagebox.showinfo("Info", "Soubor uložen do \n" + jmenoVystupnihoSouboru)

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
hodnotySeparatoru = [",", ".", ";", ":", "|", "/", "\\", "mezera", "tabulátor"]
comboboxSeparator = ttk.Combobox(mainframe, values = hodnotySeparatoru, state= "readonly")
comboboxSeparator.grid(column=0, row=0, sticky =tk.E)
comboboxSeparator.set(hodnotySeparatoru[0])

labelKodovani = ttk.Label(mainframe, text= "Kódování")
labelKodovani.grid(column=0, row=1, sticky =tk.W)
hodnotyKodovani = ["utf8", "windows-1250"]
comboboxKodovani = ttk.Combobox(mainframe, values = hodnotyKodovani)
comboboxKodovani.grid(column=0, row=1, sticky =tk.E)
comboboxKodovani.set(hodnotyKodovani[0])                                #nastaveni defaultni hodnoty

labelHlavicka = ttk.Label(mainframe, text= "Hlavička")
labelHlavicka.grid(column=0, row=2, sticky =tk.W)
hodnotyHlavicka = ["Není", "Na prvním řádku", "Zadá se ručně"]
comboboxHlavicka = ttk.Combobox(mainframe, values = hodnotyHlavicka)
comboboxHlavicka.grid(column=0, row=2, sticky =tk.E)
comboboxHlavicka.set(hodnotyHlavicka[1])                   #nastaveni defaultni hodnoty

labelRucniHlavicka = ttk.Label(mainframe, text= "Custom hlavička - názvy sloupců oddělujte čárkou")
labelRucniHlavicka.grid(column=0, row=3)
oblastRucniHlavicka = tk.Text(mainframe, height = 1, width = 80)     #tato sirka realne urcuje sirku okna
oblastRucniHlavicka.grid(column=0, row=4)

tlacitkoNahrajSoubor = ttk.Button(mainframe, text= "Nahrání souboru", command = nahrajSoubor)
tlacitkoNahrajSoubor.grid(column=0, row=5)

labelOblastiShrnuti = ttk.Label(mainframe, text = "Shrnutí")
labelOblastiShrnuti.grid(column = 0, row = 6)
oblastShrnuti = tk.Text(mainframe, height = 8, width = 80)
oblastShrnuti.config(state=tk.DISABLED)
oblastShrnuti.grid(column = 0, row = 7, sticky =tk.W)

labelPridaniKontrolaDuplicit = ttk.Label(mainframe, text = "Přidat do seznamu")
labelPridaniKontrolaDuplicit.grid(column = 0, row = 8, sticky =tk.W)
comboboxPridaniKontrolaDuplicit = ttk.Combobox(mainframe, state = "readonly")
comboboxPridaniKontrolaDuplicit.grid(column=0, row=9, sticky =tk.W)
tlacitkoPridejSloupec = ttk.Button(mainframe, text= "Přidej sloupec", command = pridejSloupec, state = tk.DISABLED)
tlacitkoPridejSloupec.grid(column=0, row=10, sticky =tk.W)

labelSeznamSloupcuDuplicity = ttk.Label(mainframe, text = "Sloupce tvořících subtabulku zkoumanou kvůli duplicitám")
labelSeznamSloupcuDuplicity.grid(column = 0, row = 8)
listboxSeznamSloupcuDuplicity  = tk.Listbox(mainframe)
listboxSeznamSloupcuDuplicity.grid(column=0, row=9)

labelOdebraniKontrolaDuplicit = ttk.Label(mainframe, text = "Odebrat ze seznamu")
labelOdebraniKontrolaDuplicit.grid(column = 0, row = 8, sticky =tk.E)
comboboxOdebraniKontrolaDuplicit = ttk.Combobox(mainframe, state = "readonly")
comboboxOdebraniKontrolaDuplicit.grid(column=0, row=9, sticky =tk.E)
tlacitkoOdeberSloupec = ttk.Button(mainframe, text= "Odeber sloupec", command = odeberSloupec, state = tk.DISABLED)
tlacitkoOdeberSloupec.grid(column=0, row=10, sticky =tk.E)

labelCoPatriDoDuplicity = ttk.Label(mainframe, text = "Duplicitou míníme")
labelCoPatriDoDuplicity.grid(column = 0, row = 11)
coJeDuplicita = tk.IntVar()    #specialni tkinterovska promenna svazujici dva radiobuttony
coJeDuplicita.set(1)           #nastaveni defaultni hodnoty na jednicku, coz odpovida volbe "Druhy a dalsi vyskyty..."
radiobuttonCoPatriDoDuplicity = ttk.Radiobutton(mainframe, text = "Druhý a další výskyty určité hodnoty", variable = coJeDuplicita, value = 1)
radiobuttonCoPatriDoDuplicity.grid(column=0, row=12)
radiobuttonCoPatriDoDuplicity = ttk.Radiobutton(mainframe, text = "Všechny výskyty určité hodnoty (včetně prvního)", variable = coJeDuplicita, value = 2)
radiobuttonCoPatriDoDuplicity.grid(column=0, row=13)

labelCoChceme = ttk.Label(mainframe, text = "Chceme")
labelCoChceme.grid(column = 0, row = 14)
coChceme = tk.IntVar()
coChceme.set(2)                              #nastaveni defaultni hodnoty na dvojku, coz odpovida volbe "Duplicitni radky"
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Unikátní řádky", variable = coChceme, value = 1)
radiobuttonCoChceme.grid(column=0, row=15)
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Duplicitní řádky", variable = coChceme, value = 2)
radiobuttonCoChceme.grid(column=0, row=16)

labelCoChceme = ttk.Label(mainframe, text = "Výsledný soubor by měly tvořit")
labelCoChceme.grid(column = 0, row = 17)
coChceme2 = tk.IntVar()
coChceme2.set(1)                                #nastaveni defaultni hodnoty na jednicku, coz odpovida volbe "Vsechny sloupce"
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Všechny sloupce", variable = coChceme2, value = 1)
radiobuttonCoChceme.grid(column=0, row=18)
radiobuttonCoChceme = ttk.Radiobutton(mainframe, text = "Jen sloupce vybrané pro určení duplicit", variable = coChceme2, value = 2)
radiobuttonCoChceme.grid(column=0, row=19)

checkBoxIndex = ttk.Checkbutton(mainframe, text = "Vložit do výsledného souboru čísla řádků")
checkBoxIndex.state(['!alternate'])                                    #aby se z checkboxu vymazal mezistav (ani zatrzene, ani nezatrzene)
checkBoxIndex.state(['selected'])                                      #aby se checkbox natvrdo nastavil do unchecked modu; bez predchoziho by to nefungovalo
checkBoxIndex.grid(column = 0, row = 20)

tlacitkoVygenerujVysledek = ttk.Button(mainframe, text= "Vygeneruj výsledný soubor", command = vygenerujVysledek, state = tk.DISABLED)
tlacitkoVygenerujVysledek.grid(column=0, row=21)

root.mainloop()  




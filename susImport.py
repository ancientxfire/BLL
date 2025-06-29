import re
import random
from funktionen.dateiAuswahl import dateiAuswahl
import pandas as pd
import numpy as np
import os 
import json

from klassen.schueler import Schueler


def zu_natürliche_zahl(wert):

    try:
        return int(wert.item()) if isinstance(wert, np.int64) else int(wert)
    except:
        return "None"
    
def extract_klassenstufe(inputStr):
    
    
    match = re.match(r'^(\d+)', inputStr)
    if match:
        return int(match.group(1))
    else:
        return None
    
'''Schülerdaten Import aus Excel Datei
'''
def susImport(klasse:int | str,excelDateiPfad:str,schuelerdatei:str):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    klassenstufe =extract_klassenstufe(klasse)
    if klassenstufe == None:
        print("ACHTUNG!!! Keine Klassenstufe in dem Sheetnamen gefunden!")
        return None
    
    if excelDateiPfad == None:
        print("keine Datei ausgewählt! Breche ab...")
        return None
    excelDatei = pd.read_excel(excelDateiPfad,klasse) 
    # Funktion nur auf numerische Spalten anwenden
    numerische_spalten = excelDatei.columns.difference(['Name'])  # 'Name'-Spalte ausschließen
    wahlen = excelDatei[numerische_spalten].map(zu_natürliche_zahl)
    neueSchülerListe = []
    for itt, name in enumerate(excelDatei["Name"]):
        wahl = []
        bewertung = {}
        wahl.append(wahlen.iloc[itt]["Wahl1"].item() if isinstance(wahlen.iloc[itt]["Wahl1"] , np.int64) else wahlen.iloc[itt]["Wahl1"])
        wahl.append(wahlen.iloc[itt]["Wahl2"].item() if isinstance(wahlen.iloc[itt]["Wahl2"], np.int64) else wahlen.iloc[itt]["Wahl2"])
        wahl.append(wahlen.iloc[itt]["Wahl3"].item() if isinstance(wahlen.iloc[itt]["Wahl3"], np.int64) else wahlen.iloc[itt]["Wahl3"])
        #bewertung[wahl[0]]=(wahlen.iloc[itt]["Bewertung1"].item() if isinstance(wahlen.iloc[itt]["Bewertung1"] , np.int64) else wahlen.iloc[itt]["Bewertung1"])
        #bewertung[wahl[1]]=(wahlen.iloc[itt]["Bewertung2"].item() if isinstance(wahlen.iloc[itt]["Bewertung2"], np.int64) else wahlen.iloc[itt]["Bewertung2"])
        #bewertung[wahl[2]]=(wahlen.iloc[itt]["Bewertung3"].item() if isinstance(wahlen.iloc[itt]["Bewertung3"], np.int64) else wahlen.iloc[itt]["Bewertung3"])
        for key in wahl:
            
            newVal = None
            try:
                newVal = random.uniform(0, 1)
            except Exception as e:
                newVal = None
                print(e)
            bewertung[key] = newVal
           
        id = name + "-" + klasse
        
        schüler = Schueler(name=name,klasse=klasse,stufe=klassenstufe,wahl=wahl,ranking=bewertung,id=id,letzteBewerbung=0)
        neueSchülerListe.append(schüler.toDict())
    
    if os.path.exists(dir_path+"/"+schuelerdatei):

        f = open(dir_path+"/"+schuelerdatei, "r")
        try:
            
            schülerListe = json.load(f)
            '''
            Hier wird die Liste schülerListe mit der Liste neueSchülerListe kombiniert. Nur Elemente aus neueSchülerListe die noch nicht in schülerListe werden in die Liste aufgenommen um Duplikate zu vermeiden.
            '''
            schülerListe = schülerListe + [data for data in neueSchülerListe if data["id"] not in schülerListe]
            f.close()
            f = open(dir_path+"/"+schuelerdatei, "w")
            f.write(json.dumps(schülerListe))
        except Exception as e:
            print(e)
            print("R/W ist fehlgeschlagen")
        finally:
            f.close()
    else:
        with open(dir_path+"/"+schuelerdatei,"a+") as f:
            f.write(json.dumps(neueSchülerListe))
            f.close()

def runSuSImport(excelDateiPfad:None|str = None,noLogging:bool = False,schuelerdatei:str = "schüler.json"):
    hatGeladen = False
    while hatGeladen == False:
        # sollte der Pfad schon per Argument gesetzt sein, wird die EIngabe übersprungen
        if excelDateiPfad == None: 
            excelDateiPfad = dateiAuswahl()
        if excelDateiPfad == None:
            print("Keine Datei ausgewählt. Breche ab.")
            break
        try:
            excelDatei = pd.ExcelFile(excelDateiPfad)
            hatGeladen = True
            klassen = excelDatei.sheet_names
            for klasse in klassen:
                if noLogging == False:
                    print(f"Import von Klasse {klasse}.")
                susImport(klasse=klasse,excelDateiPfad=excelDateiPfad,schuelerdatei=schuelerdatei)
        except Exception as e:
            print(e)
            print("\nKonnte Datei nicht lesen, wähle bitte eine neue aus.")

if __name__ == "__main__":
    runSuSImport()



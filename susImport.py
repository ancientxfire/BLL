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
    

'''Schülerdaten Import aus Excel Datei
'''
def susImport():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    klassenstufe =int(input("Klassenstufe (z.B. 10): "))
    klasse =input("Klasse oder Kurs (z.B. 10b): ")
    excelDateiPfad = dateiAuswahl()
    if excelDateiPfad == None:
        print("keine Datei ausgewählt! Breche ab...")
        return None
    excelDatei = pd.read_excel(excelDateiPfad,klasse) 
    # Funktion nur auf numerische Spalten anwenden
    numerische_spalten = excelDatei.columns.difference(['Name'])  # 'Name'-Spalte ausschließen
    wahlen = excelDatei[numerische_spalten].map(zu_natürliche_zahl)
    print(wahlen)
    neueSchülerListe = []
    for itt, name in enumerate(excelDatei["Name"]):
        wahl = []
        wahl.append(wahlen.iloc[itt]["Wahl1"].item() if isinstance(wahlen.iloc[itt]["Wahl1"] , np.int64) else wahlen.iloc[itt]["Wahl1"])
        wahl.append(wahlen.iloc[itt]["Wahl2"].item() if isinstance(wahlen.iloc[itt]["Wahl2"], np.int64) else wahlen.iloc[itt]["Wahl2"])
        wahl.append(wahlen.iloc[itt]["Wahl3"].item() if isinstance(wahlen.iloc[itt]["Wahl3"], np.int64) else wahlen.iloc[itt]["Wahl3"])
        schüler = Schueler(name=name,klasse=klasse,stufe=klassenstufe,wahl=wahl)
        neueSchülerListe.append(schüler.toDict())
    print(neueSchülerListe)
    
    if os.path.exists(dir_path+"/schüler.json"):

        f = open(dir_path+"/schüler.json", "r")
        try:
            
            schülerListe = json.load(f)
            print(schülerListe)
            '''
            Hier wird die Liste schülerListe mit der Liste neueSchülerListe kombiniert. Nur Elemente aus neueSchülerListe die noch nicht in schülerListe werden in die Liste aufgenommen um Duplikate zu vermeiden.
            '''
            schülerListe = schülerListe + [data for data in neueSchülerListe if data not in schülerListe]
            f.close()
            f = open(dir_path+"/schüler.json", "w")
            f.write(json.dumps(schülerListe))
        except Exception as e:
            print(e)
            print("R/W ist fehlgeschlagen")
        finally:
            f.close()
    else:
        with open(dir_path+"/schüler.json","a+") as f:
            f.write(json.dumps(neueSchülerListe))
            f.close()

if __name__ == "__main__":
    susImport()



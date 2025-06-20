from funktionen.dateiAuswahl import dateiAuswahl
import pandas as pd
import numpy as np
import os 
import json


NAMEN_DICT = {"Projektname":"name", "Projekt-ID":"id","Lehrkraft":"lehrkraft","Beschreibung":"beschr","Ort":"ort","Preis":"preis","max Schüler":"maxAnzahl","min Klasse":"minStufe","max Klasse":"maxStufe"}
    

'''Schülerdaten Import aus Excel Datei
'''
def projekteImport(excelDateiPfad:None|str = None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # sollte der Pfad schon per Argument gesetzt sein, wird die EIngabe übersprungen
    if excelDateiPfad == None: 
        excelDateiPfad = dateiAuswahl()
    if excelDateiPfad == None:
        print("keine Datei ausgewählt! Breche ab...")
        return None
    excelDatei = pd.ExcelFile(excelDateiPfad)
    projekteRoh = excelDatei.sheet_names
    projekte = []

    i = 0
    
    while i < len(projekteRoh):
        try: 
            daten = pd.read_excel(excelDatei,projekteRoh[i],usecols="A:B",header=None)
            datenParsed =  {}
            if len(daten.values) != 9:
                raise ValueError("Das Projekt enthält zu wenig oder zu viele Parameter")
            for elem in daten.values:
                key = NAMEN_DICT[elem[0]]
                datenParsed[key] = elem[1]
            projekte.append(datenParsed)
        except:
            print("Das " + str(i+1) +". Projekt enthält fehler!" )
        finally:
            i += 1
    print(projekte)
    if os.path.exists(dir_path+"/projekte.json"):
        
         
        
        try:
            f = open(dir_path+"/projekte.json", "r")
            jsonListe = json.load(f)
            f.close()
            k = 0
            while k < len(jsonListe):
                m = 0
                jsonProjekt = jsonListe[k]
                while m < len(projekte):
                    print(m)
                    projekt = projekte[m]
                    if jsonProjekt["id"] == projekt["id"]:
                        print(jsonProjekt["id"])
                        break
                    m += 1
                else:
                    print(jsonProjekt["id"])
                    projekte .append( jsonProjekt)
                print("Projekt",k,"fertig")
                k +=1
                
            
            f = open(dir_path+"/projekte.json", "w")
            f.write(json.dumps(projekte))
        except Exception as e:
            print(e)
            print("Schreiben ist fehlgeschlagen")
        finally:
            f.close()  
        
    else:
        with open(dir_path+"/projekte.json","a+") as f:
            projekte = [{'name': 'Platzhalter', 'id': 0, 'lehrkraft': 'NN', 'beschr': 'Platzhalter', 'ort': 'NN', 'preis': 0, 'maxAnzahl': 0, 'minStufe': 1, 'maxStufe': 4}] + projekte
            f.write(json.dumps(projekte))
            f.close() 

if __name__ == "__main__":
    projekteImport()



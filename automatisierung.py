import math
import os
import shutil
import pandas as pd
from funktionen.dateiAuswahl import dateiAuswahl
import sys
from alive_progress import alive_bar
from funktionen.dateiSpeicherOrt import dateiSpeicherOrtFrage
from main import hauptfunktion
from projekteImport import projekteImport
from susImport import runSuSImport
DATEIEN_DEFAULT = ["schüler.json","projekte.json","schülerSaveFuerV1.json"]



def automat(skipDeleteSUSQuestion = False, skipDeleteProjQuestion = False,schülerExcelDateiPfad="",projekteExcelDateiPfad="",exportPfad="",DATEIEN=DATEIEN_DEFAULT,itterationen = sys.argv[1]):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    if os.path.exists(dir_path+"/"+DATEIEN[0]) and skipDeleteSUSQuestion == False:
        eingabe1 = input("Bestätige, das du die Importierten Schüler Daten unwiderruflich löschen willst. [JA / NEIN]>> ")
        if eingabe1.lower() != "ja":

            print("DIese muss gelöscht werden, beende")
            exit()
    
    if schülerExcelDateiPfad == "":
        print("Wähle eine Schüler Excel Datei:")
        schülerExcelDateiPfad = dateiAuswahl()
        if schülerExcelDateiPfad == None:
            print("Keine Datei ausgewählt. Breche ab.")
            exit(-1)
    print(schülerExcelDateiPfad)
    eingabe2 = "ja"
    if os.path.exists(dir_path+"/"+DATEIEN[1]) and skipDeleteProjQuestion == False:
        eingabe2 = input("Bestätige, das du die Importierten Projekt Daten unwiderruflich löschen willst. [JA / NEIN]>> ")
    if eingabe2.lower() == "ja":
        if os.path.exists(dir_path+"/"+DATEIEN[1]):
            os.remove(path=dir_path+"/"+DATEIEN[1])
        if projekteExcelDateiPfad == "":
            print("Wähle eine Projekte Excel Datei:")
            projekteExcelDateiPfad = dateiAuswahl()
            print(projekteExcelDateiPfad)
            if projekteExcelDateiPfad == None:
                print("Keine Datei ausgewählt. Breche ab.")
                exit(-1)
        projekteImport(projekteExcelDateiPfad,projektedatei=DATEIEN[1])
        print("Projekte Importiert")
    else:
        print("Gespeicherte Projekte werden Verwendet")
    
    if exportPfad == "":
        exportPfad = dateiSpeicherOrtFrage(title="Ergebnisdatei")
    if exportPfad == None:
        print("Kein Export Pfad ausgewählt. Breche ab.")
        exit(-1)  
    
    print(exportPfad)
    resultate = {}
    with alive_bar(int(itterationen)) as bar:
        for i in range(int(itterationen)):
            
            if os.path.exists(dir_path+"/"+DATEIEN[0]):
                os.remove(path=dir_path+"/"+DATEIEN[0])
            runSuSImport(excelDateiPfad=schülerExcelDateiPfad,noLogging=True,schuelerdatei=DATEIEN[0]) 
            if i == 0:
                if os.path.exists(dir_path+"/"+DATEIEN[2]):
                    os.remove(path=dir_path+"/"+DATEIEN[2])
                shutil.copy2(dir_path+"/"+DATEIEN[0], dir_path+"/"+DATEIEN[2])
            projekteTopf, projekte = hauptfunktion(datenVerarbeitungUeberspringen=True)
            for itt,projekt in enumerate(projekteTopf):
                projektData = projekte[itt]
                for schüler in projekt:
                    resultate.setdefault(schüler.id, []).append((schüler.wahl.index(itt) + 1 )if itt in schüler.wahl else 4)
            
            bar()
    neuesDict = {"ID":[],}
    for i in range(int(itterationen)):
        neuesDict.setdefault(f"Itt{i}",[])
    neuesDict.setdefault("Normalisiert",[])
    for schüler,resultateListe in resultate.items():
        neuesDict["ID"].append( schüler)
        
        summeDerResultate = 0
        
        for i in range(int(itterationen)):
            neuesDict[f"Itt{i}"].append(resultateListe[i])
            summeDerResultate += resultateListe[i]
            
        
        neuesDict["Normalisiert"].append(summeDerResultate / len(resultateListe)) 
    score = 0
    niedrigsterWert = 999
    höchsterWert = 0
    for elem in neuesDict["Normalisiert"]:
        score += elem
        if niedrigsterWert > elem:
            niedrigsterWert = elem
        if höchsterWert < elem:
            höchsterWert = elem
    print("min",niedrigsterWert,"avg",score/len(neuesDict["Normalisiert"]),"max",höchsterWert)
    
    print(neuesDict["Normalisiert"][0],neuesDict["Normalisiert"][10],neuesDict["Normalisiert"][12],neuesDict["Normalisiert"][16],neuesDict["Normalisiert"][16])
    for i in range(len(neuesDict["Normalisiert"])):
        if i % 20 == 0:
            print(f"\n{i:02} - {i+19}: ",end="")
        
        print(str(neuesDict["Normalisiert"][i]).ljust(4," "),end="  ")
    print()
    with pd.ExcelWriter(exportPfad, ) as writer:
        
            
                
        dataFrame = pd.DataFrame(neuesDict)
        dataFrame = dataFrame.sort_values(by=['ID'])
        dataFrame.to_excel(writer, sheet_name=f"Resultate{itterationen}",index=False)    
    print()

RANDSUS = "C:\\Users\\ancie\\Downloads\\testdatabll\\randomSchueler.xlsx"
GEWSUS="C:\\Users\\ancie\\Downloads\\testdatabll\\gewichteteSchueler.xlsx"
PROJ25PL="C:\\Users\\ancie\\Downloads\\testdatabll\\projekteAlle25.xlsx"
PROJRANDOM="C:\\Users\\ancie\\Downloads\\testdatabll\\projekteRandomVerteilungPlaetze.xlsx"
RUNNS = [(RANDSUS,PROJ25PL,"C:\\Users\\ancie\\Downloads\\testdatabll\\projekteAlle25\\randomV2.xlsx","projekteAlle25\\exportV1Random.json"),(GEWSUS,PROJ25PL,"C:\\Users\\ancie\\Downloads\\testdatabll\\projekteAlle25\\gewichtetV2.xlsx","projekteAlle25\\exportV1Gewichtet.json")]

if __name__ == "__main__":
    automat(skipDeleteSUSQuestion = True, skipDeleteProjQuestion = True)
import os

import pandas as pd
import sys
from alive_progress import alive_bar
from funktionen.dateiSpeicherOrt import dateiSpeicherOrtFrage
from main import hauptfunktion
DATEIEN = ["schüler.json","projekte.json"]


if __name__ == "__main__":
    itterationen = sys.argv[1]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    print("Die Schüler und Projekt JSON Dateien, werden in diesem Script nicht generiert!")
    input("Bestätige mit enter!")
    exportPfad = dateiSpeicherOrtFrage(title="Ergebnisdatei")
    if exportPfad == None:
        print("Kein Export Pfad ausgewählt. Breche ab.")
        exit(-1)
    
    resultate = {}
    with alive_bar(int(itterationen)) as bar:
        for i in range(int(itterationen)):
            
             
            projekteTopf, projekte = hauptfunktion(datenVerarbeitungUeberspringen=True)
            for itt,projekt in enumerate(projekteTopf):
                projektData = projekte[itt]
                for schüler in projekt:
                    resultate.setdefault(schüler.name+ "-" +schüler.klasse, []).append((schüler.wahl.index(itt) + 1 )if itt in schüler.wahl else 4)
            bar()
    
    with pd.ExcelWriter(exportPfad, ) as writer:
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
            
                
        dataFrame = pd.DataFrame(neuesDict)
        dataFrame = dataFrame.sort_values(by=['ID'])
        dataFrame.to_excel(writer, sheet_name=f"Resultate{itterationen}",index=False)   
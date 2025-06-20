
import pandas as pd
from funktionen.dateiSpeicherOrt import dateiSpeicherOrtFrage

'''Datenverarbeitung für die Export excel Dateien
'''
def exportDatenverarbeitung(projekteTopf, alleProjekte):
    print(projekteTopf, alleProjekte)
    pfadProjekte = dateiSpeicherOrtFrage(title="Datei für Projektleiter")
    if pfadProjekte == None:
        print("Keine Datei ausgewählt! Breche ab...")
        return
    pfadKlassen = dateiSpeicherOrtFrage(title="Datei für Klassen")
    if pfadKlassen == None:
        print("Keine Datei ausgewählt! Breche ab...")
        return
    projekteProjektleiter = {}
    i = 0
    
    while i < len(projekteTopf):
        projektName = alleProjekte[i].name
        projekt = projekteTopf[i]
        projekteProjektleiter[projektName] = projekt
        i += 1
    
    with pd.ExcelWriter(pfadProjekte, ) as writer:
        i = 0
        # Für jedes Projekt wird ein Neues DataFrame erstelt. Dieses wird dann in jewails in ein Excel Sheet geschrieben.
        for projektKey in projekteProjektleiter.keys():
            projekt = projekteProjektleiter[projektKey]
            
            neuesDict = {"Name":[],"Klasse":[],"Wahl":[]}
            
            for schüler in projekt:
                                

                neuesDict["Name"].append(schüler.name)
                neuesDict["Klasse"].append(schüler.klasse)
                
                projektId = [projekt.id for projekt in alleProjekte if projekt.name == projektKey][0]
                
                neuesDict["Wahl"].append((schüler.wahl.index(projektId) + 1 )if projektId in schüler.wahl else 0)
                

                
            print(neuesDict)
            
            dataFrame = pd.DataFrame(neuesDict)
            dataFrame.to_excel(writer, sheet_name=projektKey)
    
    projekteKlassen = {}
    i = 0
    while i < len(projekteTopf):
        projektObj = alleProjekte[i]
        projekt = projekteTopf[i]
        k = 0
        while k < len(projekt):
            schüler = projekt[k]
            klasse = schüler.klasse
            neuesDict = {"schüler": schüler,"projekt":projektObj}
            if klasse in projekteKlassen.keys():
                projekteKlassen[klasse].append(neuesDict)
            else:
                projekteKlassen[klasse] = [neuesDict]
            k += 1
        i += 1
    with pd.ExcelWriter(pfadKlassen, ) as writer:
        for klasseKey in projekteKlassen.keys():
            klasse = projekteKlassen[klasseKey]
            neuesDict = {"Index":[],"Name":[],"Projekt":[],"Projektname":[],"Wahl":[]}
            for itt,schüler in enumerate(klasse):
                neuesDict["Index"].append(itt + 1)
                neuesDict["Name"].append(schüler["schüler"].name)
                neuesDict["Projekt"].append(schüler["projekt"].id)
                neuesDict["Projektname"].append(schüler["projekt"].name)
                neuesDict["Wahl"].append((schüler["schüler"].wahl.index(schüler["projekt"].id) + 1 )if schüler["projekt"].id in schüler["schüler"].wahl else 0)
            dataFrame = pd.DataFrame(neuesDict)
            dataFrame = dataFrame.sort_values(by=['Name'])
            dataFrame.to_excel(writer, sheet_name=klasseKey)            
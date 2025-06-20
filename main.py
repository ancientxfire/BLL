

import json
import os

from algo.runner import algoRunner
from funktionen.exportDatenverarbeitung import exportDatenverarbeitung
from klassen.projekt import Projekt
from klassen.schueler import Schueler

'''Hauptfunktion des Programmes welche den Algorithmus ausführt
'''
def hauptfunktion(datenVerarbeitungUeberspringen:bool = False,schuelerdatei:str = "schüler.json",projektedatei:str = "projekte.json"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(dir_path+"/"+projektedatei) == False:
        raise RuntimeError("Projekte Datei fehlt!")
    if os.path.exists(dir_path+"/"+schuelerdatei) == False:
        raise RuntimeError("Schüler Datei fehlt!")
    f = open(dir_path+"/"+projektedatei, "r")
    projekteJSON = Projekt.fromListOfDicts(json.load(f))
    f.close()
    f = open(dir_path+"/"+schuelerdatei, "r")
    schüler = Schueler.fromListOfDicts(json.load(f))
    f.close()
    projekte = []
    i = 0

    while i < len(projekteJSON):
        print("i",i)
        if projekteJSON[i].id == i:
            projekte.append(projekteJSON[i])
        else:
            k = 0
            while k < len(projekteJSON):
                print("k",k)
                if projekteJSON[k].id == i:
                    print(k,i,projekteJSON[k].id )
                    projekte.append(projekteJSON[k])
                    break
                k += 1
            else:
                raise RuntimeError("Projekt mit id", i,"nicht gefunden!")
        i += 1
    projekteTopf = algoRunner(projekte,schüler)
    print(projekteTopf, projekte)
    if datenVerarbeitungUeberspringen == False:
        exportDatenverarbeitung(projekteTopf, projekte)
    print("Fertig")
    return projekteTopf, projekte
if __name__ == "__main__":
    hauptfunktion()

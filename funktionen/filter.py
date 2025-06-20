
from klassen.schueler import Schueler
import math

def filterSuS(alleProjekte: list, alleSuS: list[Schueler]):
    i = 0
    while i < len(alleSuS):
        k = 0
        schüler = alleSuS[i]
        while k < len(schüler.wahl):
            wahl = schüler.wahl[k]
            if wahl == None:
                k += 1
                continue
            if wahl == "None":
                schüler.wahl[k] = None
                k += 1
                
                continue
            
            try:
                spezifischesProjekt = alleProjekte[wahl]
            except:
                print("Projekt existiert nicht!")
                schüler.wahl[k] = None
                k += 1
                continue
            # ----
            if schüler.stufe < spezifischesProjekt.minStufe:
                schüler.wahl[k] = None
            if schüler.stufe > spezifischesProjekt.maxStufe:
                schüler.wahl[k] = None
            k += 1
        
        """         ##Mark: WICHTIG: Diese Stelle prüft, ob die Ratings der Schüler über 9 sind. ⬇ ⬇ ⬇
        momentanerRankingTotal = 0
        
        for k,v in schüler.ranking.items():
            v = float(v)
            vOrig = v
            v = math.trunc(v)
            if momentanerRankingTotal+v > 9:
                schüler.ranking[k] = math.modf(vOrig)
            else:
                momentanerRankingTotal += v
        ## Ende der Markierten stelle                                                ⬆ ⬆ ⬆ """
        
        alleSuS[i] = schüler
        i += 1
        
    return alleSuS

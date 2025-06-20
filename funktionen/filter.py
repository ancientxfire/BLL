
def filterSuS(alleProjekte: list, alleSuS: list):
    i = 0
    while i < len(alleSuS):
        k = 0
        schüler = alleSuS[i]
        while k < len(schüler.wahl):
            wahl = schüler.wahl[k]
            if wahl == None:
                k += 1
                continue
            # ---- nicht in der , aus sicherheit hier eingefügt
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
        alleSuS[i] = schüler
        i += 1
    return alleSuS
'''Funktion: erstes Aufteilen
:param alleProjekte: Liste von allen Projekten
:param alleSuS: Liste mit allen Schülern
:param projekteTopf: Liste an Listen
'''


def erstesAufteilen(alleProjekte: list, alleSuS: list, projekteTopf: list):
    i = 0
    schülerTopf = []
    while i < len(alleSuS):
        schüler = alleSuS[i]
        wahl = schüler.wahl[0]
        if wahl == None:
            schülerTopf.append(schüler)
            i+=1
            continue
        projekteTopf[wahl].append( schüler)
        i +=1
    return schülerTopf, projekteTopf
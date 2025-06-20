'''n repräsentiert hier die Stelle der Wahl des Schülers in der Liste an Wahlen getätigt von diesem Schüler. Da es sich um eine Liste handelt fängt diese bei Stelle Null an. Das Bedeutet, dass wenn man z.B. die 2. Wahl abrufen will man als Argument für n 1 eintragen muss 
:param alleProjekte: Liste von allen Projekten
:param alleSuS: Liste mit allen Schülern
:param projekteTopf: Liste an Listen
:param schülerTopf: Liste an übrigen Schülern
:param n: nte Wahlposition
'''
def nachNterWahlSortieren(alleProjekte: list, alleSuS:list, projekteTopf: list, schülerTopf:list, n:int):
    i = len(schülerTopf) -1
    while i >= 0:
        print(i)
        schüler = schülerTopf[i]
        wahl = schüler.wahl[n]
        if wahl != None:
            mengeAnSuSImProjekt = len(projekteTopf[wahl])
            maxErlaubtImProjekt = alleProjekte[wahl].maxAnzahl
            if mengeAnSuSImProjekt < maxErlaubtImProjekt:
                projekteTopf[wahl].append(schüler)
                del schülerTopf[i]
        i -= 1
        
    return projekteTopf, schülerTopf
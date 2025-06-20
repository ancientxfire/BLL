
from utils.shuffleList import shuffleList

'''Funktion: projekteReduzieren
:param alleProjekte: Liste von allen Projekten
:param alleSuS: Liste mit allen Schülern
:param projekteTopf: Liste an Listen
:param schülerTopf: Liste an übrigen Schülern
'''
def projekteReduzieren(alleProjekte: list, alleSuS:list, projekteTopf: list, schülerTopf:list):
    i = 0
    while i < len(projekteTopf):
        projekt = alleProjekte[i]
        schülerImProjekt = projekteTopf[i]
        shuffleList(schülerImProjekt)
        k = len(schülerImProjekt) -1
        while k >= projekt.maxAnzahl:
            schülerTopf.append(schülerImProjekt[k])
            del schülerImProjekt[k]
            k -= 1
        projekteTopf[i] = schülerImProjekt
        i += 1
    return projekteTopf, schülerTopf
from klassen.projekt import Projekt
from klassen.schueler import Schueler



def freiePlätze(projektId:int,alleProjekte:list, projekteTopf:list[list]):
    """
    Gibt die Anzahl der noch freien Plätze in einem bestimmten Projekt zurück.

    Args:
        projektId (int): Die ID des Projekts.
        alleProjekte (list[Projekt]): Liste aller Projektobjekte.
        projekteTopf (list[list[Schueler]]): Liste der Teilnehmerlisten pro Projekt.

    Returns:
        int: Anzahl der freien Plätze im Projekt.
    """
    projekt = alleProjekte[projektId]
    return projekt.maxAnzahl - len(projekteTopf[projektId]) 


# Hier wird der schlechteste Score im Projekt gesucht. Die Funktion gibt den Score und den Index des schlechtesten Schülers in der TN Liste des Projekts zurück.
def schlechtesterScoreImProjekt(teilnehmer:list[Schueler],projektId:int):
    """
    Sucht den Schüler mit dem schlechtesten Ranking für ein Projekt.

    Args:
        teilnehmer (list[Schueler]): Liste der Teilnehmer eines Projekts.
        projektId (int): Die ID des Projekts.

    Returns:
        tuple[int, int]: Das schlechteste Ranking und der Index des entsprechenden Schülers.
    """
    schlechtesterScore = 10
    indexDesSchlechtestenScores = 0
    for itt, tn in enumerate(teilnehmer):
        tnRanking = tn.ranking.get(str(projektId))
        if schlechtesterScore > tnRanking:
            schlechtesterScore = tnRanking
            indexDesSchlechtestenScores = itt
    return schlechtesterScore, indexDesSchlechtestenScores


def bewerbungsschleife(alleProjekte, projekteTopf:list[list], schülerTopf: list[Schueler]):
    """
    Führt die Bewerbungslogik für Schüler aus, die ihren Projektwunsch angeben.

    Jeder Schüler bewirbt sich bis zu 3-mal. Wenn ein Projekt voll ist, wird ggf. 
    ein schlechter bewerteter Schüler ersetzt.

    Args:
        alleProjekte (list[Projekt]): Liste aller verfügbaren Projekte.
        projekteTopf (list[list[Schueler]]): Aktuelle Teilnehmerlisten für jedes Projekt.
        schülerTopf (list[Schueler]): Liste der Schüler, die noch keinem Projekt zugewiesen sind.

    Returns:
        tuple[list[list[Schueler]], list[Schueler]]: Aktualisierte Projektlisten und Restliste der Schüler.
    """
    print("beginn bewerbungsschleife")
    # Fängt von hinten an, um zu vermeiden, dass beim Löschen ein Falscher index gelöscht wird, da ein löschen in der liste die Indexe hinter diesem gelöschten Schüler ändert
    i = len(schülerTopf) - 1
    while len(schülerTopf) > 0 and any(schüler.letzteBewerbung < 3 for schüler in schülerTopf):
        schüler = schülerTopf[i]
        if (schüler.letzteBewerbung < 3):
            
            
            schülerWunsch = schüler.wahl[schüler.letzteBewerbung]
            if schülerWunsch == None:
                # Kein Wunsch vorhanden 
                schülerTopf[i].letzteBewerbung += 1
            elif freiePlätze(schülerWunsch,alleProjekte,projekteTopf) > 0:
                # Projekt nicht voll
                schüler.letzteBewerbung += 1
                projekteTopf[schülerWunsch].append(schüler)
                del schülerTopf[i]
            else:
                # Projekt voll
                schlechtesterScore,schlechtesterScoreIndex = schlechtesterScoreImProjekt(projekteTopf[schülerWunsch],schülerWunsch)
                schülerScore = schüler.ranking.get(str(schülerWunsch))
                if schlechtesterScore > schülerScore:
                    schülerTopf[i].letzteBewerbung += 1
                    # Hier wurde der Schüler abgelehnt, da der Beliebtheitsgrad des Projektes für den Schüler nicht hoch genug ist.
                else: 
                    schüler.letzteBewerbung += 1
                    schlechtererSchüler = projekteTopf[schülerWunsch][schlechtesterScoreIndex]
                    
                    del projekteTopf[schülerWunsch][schlechtesterScoreIndex]
                    # Schlechterer schüler wurde jetzt aus dem Projekt geworfen
                    projekteTopf[schülerWunsch].append(schüler)
                    del schülerTopf[i]
                    
                    schülerTopf.append(schlechtererSchüler)
        else:
            print(schüler.name,"über limit")
        i -= 1
        if i < 0:
            i = len(schülerTopf) -1
    
    print("ende bewerbungsschleife")
    return projekteTopf, schülerTopf


from algo.bewerbungsschleife import bewerbungsschleife
from algo.restlicheSuSaufGruppenAufteilen import restlicheSuSaufGruppenAufteilen
from algo.setup import setup
from funktionen.filter import filterSuS
from utils.shuffleList import shuffleList


def algoRunner(alleProjekte: list, alleSuS:list, ):
    # Filter
    alleSuS = filterSuS(alleProjekte,alleSuS)
    
    # Projektetopf erstellen
    alleProjekte, alleSuS, projekteTopf = setup(alleProjekte,alleSuS)
    schülerTopf = alleSuS
    # MARK: TODO: Noch nicht Dokumentiert 
    schülerTopf = shuffleList(schülerTopf)
    # Hauptfunktion 
    projekteTopf, schülerTopf = bewerbungsschleife(alleProjekte,projekteTopf, schülerTopf)
    # Restliche Unaufgeteilte Schüler aufteilen (Wahl 4)
    projekteTopf, schülerTopf = restlicheSuSaufGruppenAufteilen(alleProjekte, alleSuS, projekteTopf, schülerTopf)
    if len(schülerTopf) > 0:
        raise ValueError('Es sind noch SuS übrig!!')
    return projekteTopf
#MARK: TODO: Document the Function
from algo.erstesAufteilen import erstesAufteilen
from algo.projekteReduzieren import projekteReduzieren
from algo.restlicheSuSaufGruppenAufteilen import restlicheSuSaufGruppenAufteilen
from algo.setup import setup
from algo.nachNTerWahlSortieren import nachNterWahlSortieren
from funktionen.filter import filterSuS
from utils.shuffleList import shuffleList


def algoRunner(alleProjekte: list, alleSuS:list, ):
    alleSuS = filterSuS(alleProjekte,alleSuS)
    alleProjekte, alleSuS, projekteTopf = setup(alleProjekte,alleSuS)
    schülerTopf, projekteTopf = erstesAufteilen(alleProjekte, alleSuS, projekteTopf)
    projekteTopf, schülerTopf = projekteReduzieren(alleProjekte, alleSuS, projekteTopf, schülerTopf)
    schülerTopf = shuffleList(schülerTopf)
    print("Vor 2",len(schülerTopf))
    projekteTopf, schülerTopf = nachNterWahlSortieren(alleProjekte, alleSuS, projekteTopf, schülerTopf, 1)
    schülerTopf = shuffleList(schülerTopf)
    print("Vor 3",len(schülerTopf))
    projekteTopf, schülerTopf = nachNterWahlSortieren(alleProjekte, alleSuS, projekteTopf, schülerTopf, 2)
    print("Länge Schjülertopf",len(schülerTopf))
    projekteTopf, schülerTopf = restlicheSuSaufGruppenAufteilen(alleProjekte, alleSuS, projekteTopf, schülerTopf)
    print("Länge Schjülertopf",len(schülerTopf))
    if len(schülerTopf) > 0:
        raise ValueError('Es sind noch SuS übrig!!')
    return projekteTopf
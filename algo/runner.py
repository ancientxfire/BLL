#MARK: TODO: Document the Function
from algo.bewerbungsschleife import bewerbungsschleife
from algo.restlicheSuSaufGruppenAufteilen import restlicheSuSaufGruppenAufteilen
from algo.setup import setup
from funktionen.filter import filterSuS
from utils.shuffleList import shuffleList


def algoRunner(alleProjekte: list, alleSuS:list, ):
    alleSuS = filterSuS(alleProjekte,alleSuS)
    
    
    alleProjekte, alleSuS, projekteTopf = setup(alleProjekte,alleSuS)
    schülerTopf = alleSuS
    schülerTopf = shuffleList(schülerTopf)
    projekteTopf, schülerTopf = bewerbungsschleife(alleProjekte,projekteTopf, schülerTopf)
    
    projekteTopf, schülerTopf = restlicheSuSaufGruppenAufteilen(alleProjekte, alleSuS, projekteTopf, schülerTopf)
    if len(schülerTopf) > 0:
        raise ValueError('Es sind noch SuS übrig!!')
    return projekteTopf
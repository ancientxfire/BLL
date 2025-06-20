''' Funktion: Setup v1 
:param alleProjekte: Liste von allen Projekten
:param alleSuS: Liste mit allen Schülern


'''
def setup(alleProjekte: list, alleSuS: list):
    projekteTopf = []
    i = 0
    while i < len(alleProjekte):
        projekteTopf.append([])
        i += 1
    return alleProjekte, alleSuS, projekteTopf
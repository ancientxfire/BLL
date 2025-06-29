
def setup(alleProjekte: list, alleSuS: list):
    ''' Funktion: Setup v1 
    Args:
        alleProjekte (list): Liste von allen Projekten
        alleSuS (list): Liste mit allen Schülern
'''
    projekteTopf = []
    i = 0
    while i < len(alleProjekte):
        projekteTopf.append([])
        i += 1
    return alleProjekte, alleSuS, projekteTopf
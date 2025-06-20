# Definition der Klasse Schueler

import json


class Schueler:
    """Initialisierungs-Funktion der Klasse "Schueler"

    :param name: Name
    :param klasse: Klasse z.B. 9b
    :param stufe: Klassenstufe
    :param wahl: Wahl z.B. [1,5,6]
    :returns: Schueler - Self

    """
    def __init__(self, name : str, klasse: str, stufe: int, wahl: list ):
        
        self.name = name
        self.klasse = klasse
        self.stufe = stufe
        self.wahl = wahl
    
    def toDict(self):
        newMap = {}
        newMap["name"] = self.name
        newMap["klasse"] = self.klasse
        newMap["stufe"] = self.stufe
        newMap["wahl"] = self.wahl
        return newMap
        

    def fromDict(inpDict: dict):

        return Schueler(        
            inpDict["name"],
            inpDict["klasse"],
            inpDict["stufe"],
            inpDict["wahl"]
            )
    
    def fromListOfDicts(inpList: list):
        neueListe = []
        for element in inpList:
            neueListe.append(Schueler.fromDict(element))
        return neueListe
    def toString(self):
        return json.dumps(self.toDict())
    
    '''Diese Funktion erlaubt es dem 'print' Befehl die Klasse als Text zu schreiben
    
    '''
    def __str__(self):
        return json.dumps(self.toDict())
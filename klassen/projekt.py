# Definition der Klasse Projekt

import json


class Projekt:
    """Initialisierungs-Funktion der Klasse "Projekt"

    :param name: Name
    :param id: ProjektID
    :param beschr: Beschreibung
    :param ort: Ort
    :param lehrkraft: Lehrkraft
    :param maxAnzahl: Maximale Anzahl an Schülern
    :param minStufe: Niedrigste erlaubte Klassenstufe
    :param maxStufe: Höchste erlaubte Klassenstufe
    :param preis: Preis
    :returns: Projekt - Self

    """
    def __init__(self, name : str, id: int, beschr: str, ort: str, lehrkraft: str, maxAnzahl: int, minStufe: int,maxStufe: int, preis: int = 0):
        
        self.name = name
        self.id = id
        self.beschr = beschr
        self.ort = ort
        self.lehrkraft = lehrkraft
        self.maxAnzahl = maxAnzahl
        self.minStufe = minStufe
        self.maxStufe = maxStufe
        self.preis = preis
    # Objekt zu Dictionary konvertieren
    def toDict(self):
        newMap = {}
        newMap["name"] = self.name
        newMap["id"] = self.id
        newMap["beschr"] = self.beschr
        newMap["ort"] = self.ort
        newMap["lehrkraft"] = self.lehrkraft
        newMap["maxAnzahl"] = self.maxAnzahl
        newMap["minStufe"] = self.minStufe
        newMap["maxStufe"] = self.maxStufe
        newMap["preis"] = self.preis
        return newMap
        
    # Dictionary zu Objekt konvertieren
    def fromDict(inpDict: dict):

        return Projekt(        
            inpDict["name"],
            inpDict["id"],
            inpDict["beschr"], 
            inpDict["ort"],
            inpDict["lehrkraft"], 
            inpDict["maxAnzahl"],
            inpDict["minStufe"],
            inpDict["maxStufe"],
            inpDict["preis"]
            )
    # Liste an Dicts zu Liste an Objekten konvertieren
    def fromListOfDicts(inpList: list):
        neueListe = []
        for element in inpList:
            neueListe.append(Projekt.fromDict(element))
        return neueListe
    # Objekt zu String konvertieren
    def toString(self):
        return json.dumps(self.toDict())
    
    '''Diese Funktion erlaubt es dem 'print' Befehl die Klasse als Text zu schreiben
    
    '''
    def __str__(self):
        return json.dumps(self.toDict())

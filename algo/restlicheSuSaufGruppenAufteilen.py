'''Restliche SuS auf Gruppen aufteilen v1.1
:param alleProjekte: Liste von allen Projekten
:param alleSuS: Liste mit allen Schülern
:param projekteTopf: Liste an Listen
:param schülerTopf: Liste an übrigen Schülern

'''

def restlicheSuSaufGruppenAufteilen(alleProjekte: list, alleSuS:list, projekteTopf: list, schülerTopf:list):
    verfügbarePlätze = []
    i = 0
    while i < len(alleProjekte):
        projektMax = alleProjekte[i].maxAnzahl
        teilnehmerImProjekt = len(projekteTopf[i])
        projektVerfügbarePlätze = projektMax - teilnehmerImProjekt
        # Diese Variable erstellt ein Dict in welches das Schlüssel, Wert Paar geschrieben wird
        kv = {}
        kv["plätze"] = projektVerfügbarePlätze
        kv["projekt"] = alleProjekte[i]
        print(kv)
        verfügbarePlätze.append(kv)
        i += 1
    # Durch den Key parameter kann man eine FUnktion angeben, welche eine zu sortierende Zahl zurückgibt 
    verfügbarePlätze.sort(key= lambda elem: elem["plätze"],reverse=True)
    i = 0
    while i < len(verfügbarePlätze):
        print("Länge",len(schülerTopf))
        if len(schülerTopf) == 0:
            return projekteTopf, schülerTopf
        projekt = verfügbarePlätze[i]["projekt"].id
        plätze = verfügbarePlätze[i]["plätze"]
        while len(schülerTopf) > 0:
            print("Länge",len(schülerTopf))
            schüler = schülerTopf[0]
            del schülerTopf[0]
            projekteTopf[projekt].append(schüler)
            plätze -= 1
        i += 1
    return projekteTopf, schülerTopf

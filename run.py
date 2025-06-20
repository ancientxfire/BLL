from main import hauptfunktion
from neuesProjekt import altesProjektLoeschen
from projekteImport import projekteImport
from susImport import runSuSImport


OPTIONEN = {0:"Schließen",1:"Programm Starten",2:"Schüler Importieren",3:"Projekte Importieren",4:"Neues Projekt erstellen"}

if __name__ == "__main__":
    gewählteOption = None
    
    for k,v in OPTIONEN.items():
        print(f"[{k}]: {v}")
    print()
    while gewählteOption not in OPTIONEN.keys():
        print ("\033[A                             \033[A")
        try:
            gewählteOption = int(input(">> "))
        except KeyboardInterrupt:
            exit()
        except:
            continue
    
    match gewählteOption:
        case 0:
           exit(0)
        case 1:
           hauptfunktion()
        case 2:
           runSuSImport() 
        case 3:
           projekteImport() 
        case 4:
            print()
            eingabe = ""
            while eingabe.lower() not in ["ja","nein"]:
                print ("\033[A                                                                                                            \033[A")
                eingabe = input("Bestätige, das du die Importierten Daten unwiderruflich löschen willst. [JA / NEIN]>> ")
                if eingabe.lower() == "ja":
                    altesProjektLoeschen()
                elif eingabe.lower() == "nein":
                    print("Löschen abgebrochen")
                    
import { Projekt } from "./projekt";
import { Schueler } from "./schueler";

interface FreiePlaetze {
    id: number,
    anzahl: number
}

export abstract class AlgoRunner {
    finaleListe: Map<number, Schueler[]>
    schuelerOhnePlatz: Schueler[]
    constructor(public schuelerListe: Schueler[], public projekteListe: Projekt[], public maxWuensche: number = 3) {
        this.finaleListe = new Map<number, Schueler[]>()
        this.schuelerOhnePlatz = []
    }

    public run(): Map<number, Schueler[]> {
        this.filter()
        console.log("0")
        const erg = this.algo(this.schuelerListe, this.projekteListe)
        this.finaleListe = erg[0]
        this.schuelerOhnePlatz = erg[1]
        console.log("1",this.finaleListe,this.schuelerOhnePlatz.length)
        this.resteAufteilen()
        console.log("2")
        if (this.schuelerOhnePlatz.length > 0){
            throw new Error("Es gibt "+this.schuelerOhnePlatz.length+" Schüler die noch keinen Platz gefunden haben.");
            
        }
        return this.finaleListe
    }

    abstract algo(schuelerListe: Schueler[], projekteListe: Projekt[]): [Map<number, Schueler[]>, Schueler[]]

    private filter() {
        for (let index = 0; index > this.schuelerListe.length; index++) {
            const schueler: Schueler = this.schuelerListe[index];
            for (let index = 0; index < schueler.wahl.length; index++) {

                const wunschProj: Projekt | undefined = this.projekteListe.find((e) => e.id === schueler.wahl[index])
                if (wunschProj === undefined) {
                    schueler.wahl[index] = null
                }
                else if (wunschProj.maxStufe > schueler.stufe) {
                    schueler.wahl[index] = null
                }
                else if (wunschProj.minStufe < schueler.stufe) {
                    schueler.wahl[index] = null
                }

            }


            this.schuelerListe[index] = schueler
        }
    }

    private resteAufteilen() {
        let freiePlaetze: FreiePlaetze[] = []

        this.projekteListe.forEach((p) => {
            const platze = p.maxAnzahl - (this.finaleListe.get(p.id)?.length ?? 0)
            if (platze > 0) freiePlaetze.push({ id: p.id, anzahl: platze })

        })

        freiePlaetze.sort((a, b) => a.anzahl - b.anzahl)
        
        for (let index = 0; index < freiePlaetze.length; index++) {
            
            const prPl = freiePlaetze[index];
            const proj = this.projekteListe.find((p) => p.id === prPl.id)!
            
            let nochFreiInDiesemProjekt = prPl.anzahl;
            for (let index = this.schuelerOhnePlatz.length -1; index >= 0; index--) {
                if (nochFreiInDiesemProjekt <= 0) break;
                const s = this.schuelerOhnePlatz[index];
                if (!((s.stufe < proj.minStufe) || (s.stufe > proj.maxStufe))) {
                    this.finaleListe.get(proj.id)!.push(s)
                    this.schuelerOhnePlatz.splice(index,1)
                    nochFreiInDiesemProjekt--
                }
            }

        }

    }
    

}
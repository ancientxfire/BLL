import { AlgoRunner } from "./algo";
import { Projekt } from "./projekt";
import { Schueler } from "./schueler";

export class AlgoV1 extends AlgoRunner {
    algo(schuelerListe: Schueler[], projekteListe: Projekt[]): [Map<number, Schueler[]>, Schueler[]] {

        let liste = new Map<number, Schueler[]>()

        projekteListe.forEach((p) => {
            liste.set(p.id, [])
        })
        
        const schuelerTopf = [...schuelerListe]

        this.shuffle(schuelerTopf)

        // Zuteilen
        this.nachNterWahlSortieren(schuelerTopf,liste,0)
        this.nachNterWahlSortieren(schuelerTopf,liste,1)
        this.nachNterWahlSortieren(schuelerTopf,liste,2)
        return [liste, schuelerTopf]
    }
    private shuffle(array:Schueler[]) {
        for (let i = array.length - 1; i > 0; i--) {
            let j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
    private nachNterWahlSortieren(schuelerTopf: Schueler[],liste: Map<number, Schueler[]>,wahlNr:number){
        let i = schuelerTopf.length -1
        while (i>=0){
            const schueler = schuelerTopf[i]
            const wahl = schueler.wahl.at(wahlNr)
            if (typeof wahl !== "number") {
                i --
                continue
            }
            const wunschProj = this.projekteListe.find((e) => e.id === schueler.wahl[wahlNr])!
            let projAusListe = liste.get(wahl)!
            if (projAusListe!.length < wunschProj.maxAnzahl){
                projAusListe.push(schueler)
                liste.set(wahl,projAusListe)
                schuelerTopf.splice(i,1)
            }
            i --
        }
    }
}
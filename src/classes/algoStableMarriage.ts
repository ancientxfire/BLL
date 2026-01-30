import { AlgoRunner } from "./algo";
import { Projekt } from "./projekt";
import { Schueler } from "./schueler";

export class AlgoSM extends AlgoRunner {
    algo(schuelerListe: Schueler[], projekteListe: Projekt[]): [Map<number, Schueler[]>, Schueler[]] {

        let liste = new Map<number, Schueler[]>()

        projekteListe.forEach((p) => {
            liste.set(p.id, [])
        })


        let schuelerTopf = schuelerListe
        let schuelerOhnePlatz = []
        let i = schuelerTopf.length - 1
        while (schuelerTopf.length > 0) {
            let schueler = schuelerTopf[i]

            if (schueler.letzteBewerbung >= 3) {
                // Fall 0
                console.log("AAA Fall 0", schueler.letzteBewerbung)
                schuelerOhnePlatz.push(schueler)
                schuelerTopf.splice(i, 1)
            } else {
                console.log(schueler)
                const schuelerWunsch = schueler.wahl[schueler.letzteBewerbung]

                if (schuelerWunsch === null) {
                    // Fall 1
                    schueler.letzteBewerbung += 1
                } else if (liste.get(schuelerWunsch)!.length < projekteListe.find((p) => p.id === schuelerWunsch)!.maxAnzahl) {
                    // Fall 2
                    liste.get(schuelerWunsch)!.push(schueler)
                    schuelerTopf.splice(i, 1)
                } else {
                    console.log("Fall 3 / 4")
                    let schuelerImProjekt = liste.get(schuelerWunsch)!
                    let niedrigsterScore = 1
                    let niedrigsterScoreInd: number | undefined = undefined
                    for (let index = 0; index < schuelerImProjekt.length; index++) {
                        const sImProj = schuelerImProjekt[index];
                        if (sImProj.ranking[schuelerWunsch] < niedrigsterScore) {
                            niedrigsterScore = sImProj.ranking[schuelerWunsch]
                            niedrigsterScoreInd = index
                        }
                    }
                    console.log("AAA", niedrigsterScore, niedrigsterScoreInd)
                    if (schueler.ranking[schuelerWunsch] <= niedrigsterScore) {
                        // Fall 3
                        schueler.letzteBewerbung += 1
                        console.log("AAA Fall 3", schuelerWunsch)
                    } else if (schueler.ranking[schuelerWunsch] > niedrigsterScore) {
                        // Fall 4
                        console.log("AAA Fall 4", schuelerWunsch, schueler.letzteBewerbung)
                        schueler.letzteBewerbung += 1
                        const schlechtesterSchueler = schuelerImProjekt[niedrigsterScoreInd!]
                        let a = liste.get(schuelerWunsch)!
                        a.splice(niedrigsterScoreInd!, 1)
                        liste.set(schuelerWunsch, a)

                        let b = liste.get(schuelerWunsch)!
                        b.push(schueler)
                        liste.set(schuelerWunsch, b)
                        schuelerTopf.splice(i, 1)
                        console.error("AAA", schuelerTopf.length)
                        schuelerTopf.push(schlechtesterSchueler)
                        console.error("AAA", schuelerTopf.length)
                    }
                }
            }




            schuelerTopf[i] = schueler
            i--
            if (i < 0) {
                i = schuelerTopf.length - 1
                if (this.hatSchuelerUnter3(schuelerTopf) === false) {
                    break
                }
            }

        }




        return [liste, schuelerOhnePlatz]
    }
    private hatSchuelerUnter3(schuelerTopf: Schueler[]): boolean {
        if (schuelerTopf.length === 0) return true
        return (schuelerTopf.filter((s) => s.letzteBewerbung < 3).length > 0)
    }

}
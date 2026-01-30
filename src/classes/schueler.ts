/**
 * Interface für die Schüler-Daten
 */
export interface SchuelerData {
  name: string;
  klasse: string;
  stufe: number;
  wahl: (number | null)[];
  ranking: Record<string, number>; // Entspricht dict in Python (Key: ID, Value: Score)
  id: string;
  letzteBewerbung: number;
}

/**
 * Klasse Schueler
 */
export class Schueler implements SchuelerData {
  constructor(
    public name: string,
    public klasse: string,
    public stufe: number,
    public wahl: (number | null)[],
    public ranking: Record<string, number>,
    public id: string,
    public letzteBewerbung: number
  ) {}

  /**
   * Wandelt das Objekt in ein Plain Object (Dictionary) um
   */
  toDict(): SchuelerData {
    return {
      name: this.name,
      klasse: this.klasse,
      stufe: this.stufe,
      wahl: this.wahl,
      ranking: this.ranking,
      id: this.id,
      letzteBewerbung: this.letzteBewerbung,
    };
  }

  /**
   * Erstellt eine Schueler-Instanz aus einem Dictionary
   */
  static fromDict(inpDict: SchuelerData): Schueler {
    return new Schueler(
      inpDict.name,
      inpDict.klasse,
      inpDict.stufe,
      inpDict.wahl,
      inpDict.ranking,
      inpDict.id,
      inpDict.letzteBewerbung
    );
  }
  static fromString(jsonString: string): Schueler {
    const data = JSON.parse(jsonString);
    return Schueler.fromDict(data);
  }
  /**
   * Konvertiert eine Liste von Dicts in eine Liste von Schueler-Instanzen
   */
  static fromListOfDicts(inpList: SchuelerData[]): Schueler[] {
    return inpList.map((element) => Schueler.fromDict(element));
  }

  /**
   * Entspricht __str__ / toString
   */
  toString(): string {
    return JSON.stringify(this.toDict());
  }
}
/**
 * Interface für die Typisierung der Rohdaten
 */
export interface ProjektData {
  name: string;
  id: number;
  beschr: string;
  ort: string;
  lehrkraft: string;
  maxAnzahl: number;
  minStufe: number;
  maxStufe: number;
  preis: number;
}

/**
 * Die Projekt-Klasse
 * Durch das "export" kann sie in .vue oder .ts Dateien importiert werden.
 */
export class Projekt implements ProjektData {
  constructor(
    public name: string,
    public id: number,
    public beschr: string,
    public ort: string,
    public lehrkraft: string,
    public maxAnzahl: number,
    public minStufe: number,
    public maxStufe: number,
    public preis: number = 0
  ) {}

  toDict(): ProjektData {
    return {
      name: this.name,
      id: this.id,
      beschr: this.beschr,
      ort: this.ort,
      lehrkraft: this.lehrkraft,
      maxAnzahl: this.maxAnzahl,
      minStufe: this.minStufe,
      maxStufe: this.maxStufe,
      preis: this.preis,
    };
  }

  static fromDict(inpDict: ProjektData): Projekt {
    return new Projekt(
      inpDict.name,
      inpDict.id,
      inpDict.beschr,
      inpDict.ort,
      inpDict.lehrkraft,
      inpDict.maxAnzahl,
      inpDict.minStufe,
      inpDict.maxStufe,
      inpDict.preis ?? 0
    );
  }
  static fromString(jsonString: string): Projekt {
    return Projekt.fromDict(JSON.parse(jsonString));
  }
  static fromListOfDicts(inpList: ProjektData[]): Projekt[] {
    return inpList.map((element) => Projekt.fromDict(element));
  }

  toString(): string {
    return JSON.stringify(this.toDict());
  }
}
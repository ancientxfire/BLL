import * as XLSX from 'xlsx';
import { Schueler, type SchuelerData } from "../classes/schueler";

/**
 * Verarbeitet mehrere Excel-Dateien und gibt eine konsolidierte Liste von Schülern zurück.
 * Effizienz: O(n) durch Verwendung eines Sets für den Duplikat-Check.
 */
export const processExcelFiles = async (
  files: File[], 
  existingSchueler: SchuelerData[] = []
): Promise<SchuelerData[]> => {
  const resultList: SchuelerData[] = [...existingSchueler];
  const idSet = new Set(existingSchueler.map(s => s.id));

  // Wir nutzen Promise.all, um die Dateien theoretisch parallel zu laden
  const filePromises = files.map(async (file) => {
    const data = await file.arrayBuffer();
    const workbook = XLSX.read(data, { type: 'array' });

    for (const sheetName of workbook.SheetNames) {
      const klassenstufeMatch = sheetName.match(/^(\d+)/);
      if (!klassenstufeMatch) continue;

      const stufe = parseInt(klassenstufeMatch[1], 10);
      const rows = XLSX.utils.sheet_to_json<any>(workbook.Sheets[sheetName]);

      for (const row of rows) {
        if (!row.Name) continue;
        let name = ""
        let vorname = ""
        let nachname = ""
        let id = ""
        if (row.Vorname && row.nachname) {
          id = `${row.Vorname}-${row.Nachname}-${sheetName}`;
          vorname = row.Vorname
          nachname = row.Nachname
          name = vorname + " " + nachname
        } else if (row.Name) {
          id = `${(row.Name as string).trim().replace(' ',"-") }-${sheetName}`;
          name = row.Name
        } else continue
        
        if (idSet.has(id)) continue;

        // Wahlen extrahieren
        const wahl = [
          row.Wahl1 ? parseInt(row.Wahl1, 10) : null,
          row.Wahl2 ? parseInt(row.Wahl2, 10) : null,
          row.Wahl3 ? parseInt(row.Wahl3, 10) : null
        ];

        // Ranking Map (Score zwischen 0 und 1)
        const ranking: Record<string, number> = {};
        wahl.forEach(w => {
          if (w !== null) ranking[w.toString()] = Math.random();
        });

        const neuerSchueler = new Schueler(
          name,
          sheetName,
          stufe,
          wahl,
          ranking,
          id,
          0,
          vorname,
          nachname
        );

        resultList.push(neuerSchueler.toDict());
        idSet.add(id);
      }
    }
  });

  await Promise.all(filePromises);
  return resultList;
};
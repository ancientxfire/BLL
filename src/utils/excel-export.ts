import * as XLSX from 'xlsx';
import type { Schueler } from '../classes/schueler';
import type { Projekt } from '../classes/projekt';

export const exportResults = (resultMap: Map<number, Schueler[]>, alleProjekte: Projekt[]) => {
  // --- 1. PROJEKTLEITER DATEI ---
  const wbProjekte = XLSX.utils.book_new();

  // Wir iterieren über alle Projekte, um auch leere Projekte anzuzeigen 
  // oder nur die, die Schüler haben (wie im Python Script)
  resultMap.forEach((schuelerListe, projektId) => {
    // Finde das zugehörige Projekt-Objekt für den Namen
    const projektObj = alleProjekte.find(p => Number(p.id) === Number(projektId));
    const projektName = projektObj?.name || `Projekt ${projektId}`;

    // Daten für dieses Projekt vorbereiten
    const sheetData = schuelerListe.map(schueler => {
      // Wahl-Logik wie im Python Script (index + 1 oder 0)
      const wahlIndex = schueler.wahl.indexOf(projektId);
      const wahlErgebnis = wahlIndex !== -1 ? wahlIndex + 1 : 0;

      return {
        'Name': schueler.name,
        'Klasse': schueler.klasse,
        'Wahl': wahlErgebnis
      };
    });

    // Sheet erstellen und hinzufügen (max 31 Zeichen für Sheetnamen)
    const ws = XLSX.utils.json_to_sheet(sheetData);
    XLSX.utils.book_append_sheet(wbProjekte, ws, projektName.substring(0, 31));
  });

  // Download triggern
  XLSX.writeFile(wbProjekte, "Zuweisung_Projektleiter.xlsx");


  // --- 2. KLASSEN DATEI ---
  const wbKlassen = XLSX.utils.book_new();
  const klassenStruktur: Record<string, any[]> = {};

  // Daten nach Klassen gruppieren (wie in Python: projekteKlassen[klasse])
  resultMap.forEach((schuelerListe, projektId) => {
    const projektObj = alleProjekte.find(p => Number(p.id) === Number(projektId));

    schuelerListe.forEach(schueler => {
      const klasse = schueler.klasse;
      if (!klassenStruktur[klasse]) {
        klassenStruktur[klasse] = [];
      }

      const wahlIndex = schueler.wahl.indexOf(projektId);
      const wahlErgebnis = wahlIndex !== -1 ? wahlIndex + 1 : 0;

      klassenStruktur[klasse].push({
        'Name': schueler.name,
        'Projekt': projektId,
        'Projektname': projektObj?.name || 'Unbekannt',
        'Wahl': wahlErgebnis
      });
    });
  });

  // Für jede Klasse ein Sheet erstellen
  Object.keys(klassenStruktur).forEach(klasseKey => {
    let rows = klassenStruktur[klasseKey];

    // Sortierung nach Name (wie Python: dataFrame.sort_values(by=['Name']))
    rows.sort((a, b) => a.Name.localeCompare(b.Name));

    const ws = XLSX.utils.json_to_sheet(rows);
    XLSX.utils.book_append_sheet(wbKlassen, ws, klasseKey.substring(0, 31));
  });

  // Download triggern
  XLSX.writeFile(wbKlassen, "Zuweisung_Klassen.xlsx");
};
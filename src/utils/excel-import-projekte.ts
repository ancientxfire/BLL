import * as XLSX from 'xlsx';
import { Projekt, type ProjektData } from '../classes/projekt';


	const NAMEN_MAP: Record<string, keyof ProjektData> = {
	  "Projektname": "name",
	  "Projekt-ID": "id",
	  "Lehrkraft": "lehrkraft",
	  "Beschreibung": "beschr",
	  "Ort": "ort",
	  "Preis": "preis",
	  "max Schüler": "maxAnzahl",
	  "min Klasse": "minStufe",
	  "max Klasse": "maxStufe"
	};
	
	export const processProjektFiles = async (
	  files: File[],
	  existingProjekte: ProjektData[] = []
	): Promise<ProjektData[]> => {
	  const idSet = new Set(existingProjekte.map(p => p.id));
	  const resultList: ProjektData[] = [...existingProjekte];
	
	  for (const file of files) {
	    const buffer = await file.arrayBuffer();
	    const workbook = XLSX.read(buffer, { type: 'array' });
	
	    for (const sheetName of workbook.SheetNames) {
	      try {
	        const sheet = workbook.Sheets[sheetName];
	        const rows = XLSX.utils.sheet_to_json<any[]>(sheet, { header: 1 });
	
	        // Wir initialisieren ein leeres Objekt und casten es zu any für den Aufbau,
	        // um den "assignable to undefined" Fehler zu umgehen.
	        const datenParsed: any = {};
	        
	        for (const row of rows) {
	          if (!row || row.length < 2) continue;
	          
	          const excelKey = String(row[0]).trim();
	          const value = row[1];
	          
	          const dataKey = NAMEN_MAP[excelKey];
	          if (dataKey) {
	            if (['id', 'preis', 'maxAnzahl', 'minStufe', 'maxStufe'].includes(dataKey)) {
	              // Sicherstellen, dass es eine Zahl wird
	              datenParsed[dataKey] = typeof value === 'number' ? value : parseFloat(value) || 0;
	            } else {
	              datenParsed[dataKey] = String(value);
	            }
	          }
	        }
	
	        // Prüfen, ob die ID vorhanden ist und alle Felder (9 Stück) gemappt wurden
	        if (datenParsed.id !== undefined && Object.keys(datenParsed).length >= 9) {
	          if (!idSet.has(datenParsed.id)) {
	            // Erst hier casten wir es sicher in das Interface
	            const projektFinal = Projekt.fromDict(datenParsed as ProjektData);
	            resultList.push(projektFinal.toDict());
	            idSet.add(datenParsed.id);
	          }
	        }
	      } catch (err) {
	        console.error(`Fehler im Sheet ${sheetName}:`, err);
	      }
	    }
	  }
	
	  if (resultList.length === 0 && existingProjekte.length === 0) {
	    resultList.push({
	      name: 'Platzhalter', id: 0, lehrkraft: 'NN', beschr: 'Platzhalter', 
	      ort: 'NN', preis: 0, maxAnzahl: 0, minStufe: 1, maxStufe: 4
	    });
	  }
	
	  return resultList;
	};
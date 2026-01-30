import { type ProjektData } from "./projekt";
import { type SchuelerData } from './schueler';

export const TEST_PROJEKTE_RAW: ProjektData[] = [
  {
    name: "Robotik mit LEGO Spike",
    id: 101,
    beschr: "Baue und programmiere eigene Roboter.",
    ort: "Informatikraum 1",
    lehrkraft: "Hr. Weber",
    maxAnzahl: 15,
    minStufe: 5,
    maxStufe: 9,
    preis: 5
  },
  {
    name: "Theater-Workshop",
    id: 102,
    beschr: "Inszenierung eines modernen Dramas.",
    ort: "Aula",
    lehrkraft: "Fr. Meier",
    maxAnzahl: 20,
    minStufe: 9,
    maxStufe: 13,
    preis: 0
  },
  {
    name: "Alpenüberquerung (Vorbereitung)",
    id: 103,
    beschr: "Physische Vorbereitung und Routenplanung.",
    ort: "Sporthalle",
    lehrkraft: "Hr. Sportlich",
    maxAnzahl: 12,
    minStufe: 11,
    maxStufe: 13,
    preis: 50
  }
];

export const TEST_SCHUELER_RAW: SchuelerData[] = [
  {
      name: "Matthias Müller",
      klasse: "13Q2",
      stufe: 13,
      wahl: [103, 102, null],
      id: "S-78945",
      letzteBewerbung: 0,
      ranking: {103:0.2,102:0.1,101:0.9}
  },
  {
      name: "Sophie Schmidt",
      klasse: "6b",
      stufe: 6,
      wahl: [101, null, null],
      id: "S-12345",
      letzteBewerbung: 0,
      ranking: {103:0.3,102:0.05,101:0.4}
  },
  {
      name: "Lukas Läufer",
      klasse: "11a",
      stufe: 11,
      wahl: [103, 101, 102],
      id: "S-55443",
      letzteBewerbung: 0,
      ranking: {103:0.4,102:0.98,101:0.2}
  }
];
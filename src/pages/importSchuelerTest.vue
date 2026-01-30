<template>
  <UContainer class="py-10 space-y-6">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Projekt-Zuweisung (Stable Marriage)</h1>
        <p class="text-sm text-gray-500">Lade zuerst die Daten hoch, um die Berechnung zu starten.</p>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Input Schüler -->
        <div class="space-y-2">
          <label class="text-sm font-medium">1. Schüler-Listen (Excel)</label>
          <UFileUpload
            multiple
            accept=".xlsx"
            icon="i-heroicons-users"
            @update:model-value="onSchuelerUpload"
          />
          <UBadge v-if="rawSchueler.length" color="success" variant="subtle">
            {{ rawSchueler.length }} Schüler geladen
          </UBadge>
        </div>

        <!-- Input Projekte -->
        <div class="space-y-2">
          <label class="text-sm font-medium">2. Projekt-Definitionen (Excel)</label>
          <UFileUpload
            multiple
            accept=".xlsx"
            icon="i-heroicons-briefcase"
            @update:model-value="onProjektUpload"
          />
          <UBadge v-if="rawProjekte.length" color="success" variant="subtle">
            {{ rawProjekte.length }} Projekte geladen
          </UBadge>
        </div>
      </div>

      <template #footer>
        <div class="flex gap-4">
          <UButton 
            :disabled="!canRun" 
            icon="i-heroicons-play" 
            block 
            class="flex-1"
            @click="algosm"
          >
            Algorithmus ausführen
          </UButton>
          <UButton 
            v-if="output.size > 0" 
            icon="i-heroicons-document-arrow-down" 
            color="success" 
            variant="outline"
            @click="downloadExcel"
          >
            Ergebnisse exportieren
          </UButton>
        </div>
      </template>
    </UCard>

    <!-- Ergebnis-Anzeige -->
    <div v-if="output.size > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard v-for="[id, liste] in output.entries()" :class="(((liste.length-(getProjektByID(id).maxAnzahl))>0)? ' animate-pulse bg-red-600' : '')" :key="id" size="sm">
        <template #header >
          <div :class="'flex justify-between items-center'">
            <span class="font-bold">{{ getProjektByID(id).name }} </span>
            <span class="text-xs text-gray-500">{{ liste.length }} Personen von {{ getProjektByID(id).maxAnzahl }}</span>
          </div>
        </template>
        <div class="text-sm space-y-1">
          <div v-for="s in liste" :key="s.id" class="flex justify-between">
            <span>{{ s.name }}</span>
            <span>{{ s.wahl }}</span>
            <span class="text-gray-400 text-xs">{{ s.klasse }}</span>
          </div>
        </div>
      </UCard>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { processExcelFiles } from '../utils/excel-import-schueler';
import { processProjektFiles } from '../utils/excel-import-projekte';
import { exportResults } from '../utils/excel-export';
import { AlgoSM } from '../classes/algoStableMarriage';
import { Schueler, type SchuelerData } from '../classes/schueler';
import { Projekt, type ProjektData } from '../classes/projekt';

const rawSchueler = ref<SchuelerData[]>([]);
const rawProjekte = ref<ProjektData[]>([]);
const output = ref<Map<number, Schueler[]>>(new Map());

const canRun = computed(() => rawSchueler.value.length > 0 && rawProjekte.value.length > 0);

// Handlers für Datei-Uploads
const onSchuelerUpload = async (files: File[] | null | undefined) => {
  if (!files) return;
  rawSchueler.value = await processExcelFiles(files, rawSchueler.value);
  console.log(rawSchueler)
};

const onProjektUpload = async (files: File[] | null | undefined) => {
  if (!files) return;
  rawProjekte.value = await processProjektFiles(files, rawProjekte.value);
  console.log(rawProjekte)
};

function algosm() {
  const schuelerInstanzen = Schueler.fromListOfDicts(rawSchueler.value);
  const projektInstanzen = Projekt.fromListOfDicts(rawProjekte.value);

  const algo = new AlgoSM(schuelerInstanzen, projektInstanzen);
  output.value = algo.run();
  let anzSchueler = 0
  output.value.forEach((v)=>{
    anzSchueler += v.length
  })

  useToast().add({ title: 'Berechnung abgeschlossen',description:"Anz Schüler: "+anzSchueler, color: 'success' });
}

function getProjektByID(id:number){
  return rawProjekte.value.find((p)=>p.id === id)!
}

function downloadExcel() {
  const projektInstanzen = Projekt.fromListOfDicts(rawProjekte.value);
  exportResults(output.value, projektInstanzen);
}
</script>
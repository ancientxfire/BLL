<template>
  <UContainer class="py-10 space-y-6">
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Projekt-Zuweisung ({{ algoInfos[($route.params.algo as string)]["name"] }})</h1>
        <p class="text-sm text-gray-500">Lade zuerst die Daten hoch, um die Berechnung zu starten.</p>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Input Schüler -->
        <div class="space-y-2">
          <label class="text-sm font-medium">1. Schüler-Listen (Excel)</label>
          <UFileUpload multiple accept=".xlsx" icon="i-heroicons-users" @update:model-value="onSchuelerUpload" />
          <UBadge v-if="rawSchueler.length" color="success" variant="subtle">
            {{ rawSchueler.length }} Schüler geladen
          </UBadge>
        </div>

        <!-- Input Projekte -->
        <div class="space-y-2">
          <label class="text-sm font-medium">2. Projekt-Definitionen (Excel)</label>
          <UFileUpload multiple accept=".xlsx" icon="i-heroicons-briefcase" @update:model-value="onProjektUpload" />
          <UBadge v-if="rawProjekte.length" color="success" variant="subtle">
            {{ rawProjekte.length }} Projekte geladen
          </UBadge>
        </div>
      </div>

      <template #footer>
        <div class="flex gap-4">
          <UButton :loading="isRunning" :disabled="!canRun" icon="i-heroicons-play" block class="flex-1"
            @click="algoStarter(($route.params.algo as string))">
            Algorithmus ausführen
          </UButton>
          <UButton v-if="output.size > 0" icon="i-heroicons-document-arrow-down" color="success" variant="outline"
            @click="downloadExcel">
            Ergebnisse exportieren
          </UButton>
        </div>
      </template>
    </UCard>

    <!-- Ergebnis-Anzeige -->
    <div v-if="output.size > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <UCard v-for="[id, liste] in output.entries()" :key="id"
        :class="liste.length > getProjektByID(id).maxAnzahl ? 'ring-2 ring-red-500 animate-pulse' : ''" size="sm">
        <template #header>
          <div class="flex justify-between items-center">
            <span class="font-bold">{{ getProjektByID(id).name }}</span>
            <span class="text-xs text-gray-500">
              {{ liste.length }} / {{ getProjektByID(id).maxAnzahl }}
            </span>
          </div>
        </template>

        <div class="text-sm space-y-2">
          <!-- Hintergrund angepasst für Darkmode Kompatibilität -->
          <div v-for="s in liste" :key="s.id"
            class="flex items-center justify-between bg-neutral-100 dark:bg-neutral-800 p-2 rounded-lg border border-neutral-200 dark:border-neutral-700">
            <div class="flex flex-col">
              <span class="font-medium text-neutral-900 dark:text-white">{{ s.name }}</span>
              <span class="text-[10px] text-neutral-500 dark:text-neutral-400">
                Wahl: {{ s.wahl }} | {{ s.klasse }}
              </span>
            </div>

            <USelectMenu :items="rawProjekte.filter(p => p.id !== id)" label-key="name" value-key="id"
              :ui="{ content: 'w-64' }" @update:model-value="(newProjId) => moveStudent(s, id, Number(newProjId))">
              <UButton icon="i-heroicons-arrows-right-left" size="xs" color="neutral" variant="subtle" />
            </USelectMenu>
          </div>
        </div>
      </UCard>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { processExcelFiles } from '../utils/excel-import-schueler';
import { processProjektFiles } from '../utils/excel-import-projekte';
import { exportResults } from '../utils/excel-export';
import { AlgoSM } from '../classes/algoStableMarriage';
import { Schueler, type SchuelerData } from '../classes/schueler';
import { Projekt, type ProjektData } from '../classes/projekt';
import { useRoute, useRouter } from 'vue-router';
import { AlgoV1 } from '../classes/algoGreedyV1';

const rawSchueler = ref<SchuelerData[]>([]);
const rawProjekte = ref<ProjektData[]>([]);
const output = ref<Map<number, Schueler[]>>(new Map());
const isRunning = ref<boolean>(false)
const algoList = ["sma", "v1"]
const algoInfos: Record<string, Record<string, any>> = { "sma": { name: "Stable Marriage" }, "v1": { name: "Version 1 der BLL" } }

const canRun = computed(() => rawSchueler.value.length > 0 && rawProjekte.value.length > 0);

const onSchuelerUpload = async (files: File[] | null | undefined) => {
  if (!files) return;
  rawSchueler.value = await processExcelFiles(files, rawSchueler.value);
};

const onProjektUpload = async (files: File[] | null | undefined) => {
  if (!files) return;
  rawProjekte.value = await processProjektFiles(files, rawProjekte.value);
};

// Prüft, ob schon Ergebnisse vorhanden sind und fragt den User, ob er den Algo ausführen möchte
function algoStarter(algo: string) {
  if (output.value.size > 0) {
    useToast().add({
      title: 'Der Algo wurde schon ausgeführt, nochmal ausführen?',
      actions: [{
        icon: 'i-lucide-refresh-cw',
        label: 'Nochmal Ausführen',
        color: 'warning',
        variant: 'outline',
        onClick: () => {
          runAlgo(algo)
        }
      }]
    })
  }
  else {
    runAlgo(algo)
  }
}

function runAlgo(algo: string) {
  isRunning.value = true
  const schuelerInstanzen = Schueler.fromListOfDicts(rawSchueler.value);
  const projektInstanzen = Projekt.fromListOfDicts(rawProjekte.value);


  try {
    if (algo === "sma") {
      const algo = new AlgoSM(schuelerInstanzen, projektInstanzen);
      output.value = algo.run();
    } else if (algo === "v1") {
      const algo = new AlgoV1(schuelerInstanzen, projektInstanzen);
      output.value = algo.run();
    } else {
      isRunning.value = false
      useToast().add({ title: 'Kein valider Algo ausgewählt', color: 'error' });
      return
    }
    useToast().add({ title: 'Berechnung abgeschlossen', description: algo, color: 'success' });
  } catch (error) {
    useToast().add({ title: `${error}`, color: 'error' });
    console.error(error)

  }


  isRunning.value = false
}

/**
 * Verschiebt einen Schüler manuell in ein anderes Projekt
 */
function moveStudent(schueler: Schueler, oldProjectId: number, newProjectId: number) {
  const oldList = output.value.get(oldProjectId);
  const newList = output.value.get(newProjectId);

  if (oldList && newList) {
    // 1. Aus alter Liste entfernen
    const index = oldList.findIndex(s => s.id === schueler.id);
    if (index !== -1) {
      oldList.splice(index, 1);
    }
    // 2. In neue Liste einfügen
    newList.push(schueler);

    // UI Feedback
    useToast().add({
      title: 'Verschoben',
      description: `${schueler.name} ist jetzt in ${getProjektByID(newProjectId).name}`,
      color: 'primary'
    });
  }
}

function getProjektByID(id: number) {
  return rawProjekte.value.find((p) => p.id === id) || { name: 'Unbekannt', maxAnzahl: 0 };
}

function downloadExcel() {
  const projektInstanzen = Projekt.fromListOfDicts(rawProjekte.value);
  exportResults(output.value, projektInstanzen);
}

onBeforeMount(() => {
  const algo: string = useRoute().params.algo as string

  if (!algoList.includes(algo)) {
    useToast().add({ title: "Dieser Algo ist nicht bekannt!", description: "Der Algo wurde zu SM gewechselt", color: "error" })
    return useRouter().push({ path: '/sma' })
  }
})
</script>
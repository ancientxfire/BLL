<template>
<div>
  <UButton @click="algosm()">Run SM</UButton>
  <div v-for="[k,v] in output.entries()">
    <UCard>
      <template #header>{{ k }}</template>
      <div v-for="s in v">
        <p>{{ s }}</p>
      </div>
    </UCard>
  </div>
</div>
</template>

<script setup lang="ts">

import { ref } from 'vue';
import { processExcelFiles } from '../utils/excel-import-schueler';
import { processProjektFiles } from '../utils/excel-import-projekte';

import { AlgoSM } from '../classes/algoStableMarriage';
import { Projekt, ProjektData } from '../classes/projekt';
import { Schueler,SchuelerData } from '../classes/schueler';
import * as testData from '../classes/testData'

const output = ref<Map<number, Schueler[]>>(new Map<number, Schueler[]>)

function algosm() {
  let algo = new AlgoSM(Schueler.fromListOfDicts(testData.TEST_SCHUELER_RAW),Projekt.fromListOfDicts(testData.TEST_PROJEKTE_RAW))
  let result = algo.run()
  console.log(result)
  output.value = result
  
  
}

</script>
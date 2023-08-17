<template>
  <q-timeline-entry>
    <text-button
      v-if="!addOpen"
      block
      color="primary"
      label="Add Model Training"
      @click="addOpen = true"
    />
    <panel-card v-else>
      <tab-list v-model="tab" :tabs="tabs">
        <template #documents>
          <model-document-step :model="props.model" @submit="addOpen = false" />
        </template>
        <template #repositories>
          <model-repository-step
            :model="props.model"
            @submit="addOpen = false"
          />
        </template>
        <template #keywords>
          <model-keywords-step :model="props.model" @submit="addOpen = false" />
        </template>
        <template #project>
          <model-project-step :model="props.model" @submit="addOpen = false" />
        </template>
      </tab-list>
    </panel-card>
  </q-timeline-entry>
</template>

<script lang="ts">
/**
 * Displays inputs for training a model.
 */
export default {
  name: "ModelTrainingCreator",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { GenerationModelProps } from "@/types";
import { trainingTabOptions } from "@/util";
import { TabList, TextButton, PanelCard } from "@/components/common";
import {
  ModelProjectStep,
  ModelDocumentStep,
  ModelRepositoryStep,
  ModelKeywordsStep,
} from "./steps";

const props = defineProps<GenerationModelProps>();

const tabs = trainingTabOptions();

const tab = ref("documents");
const addOpen = ref(false);
</script>

<template>
  <q-timeline-entry>
    <text-button
      v-if="!addOpen"
      block
      color="primary"
      label="Add Model Training"
      @click="addOpen = true"
    />
    <q-card v-else bordered flat class="q-pa-md">
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
    </q-card>
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
import { GenerationModelSchema } from "@/types";
import { trainingTabOptions } from "@/util";
import { TabList } from "@/components/common";
import TextButton from "@/components/common/button/TextButton.vue";
import {
  ModelProjectStep,
  ModelDocumentStep,
  ModelRepositoryStep,
  ModelKeywordsStep,
} from "./steps";

const props = defineProps<{
  model: GenerationModelSchema;
}>();

const tabs = trainingTabOptions();

const tab = ref("documents");
const addOpen = ref(false);
</script>

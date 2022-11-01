<template>
  <v-timeline-item color="primary lighten-3" small>
    <v-btn v-if="!addOpen" block color="primary" @click="addOpen = true">
      Add Model Training
    </v-btn>
    <v-card v-else outlined class="pa-2">
      <v-container style="max-width: 40em">
        <v-select
          filled
          hide-details
          label="Training Type"
          :items="trainingOptions"
          v-model="trainingType"
        />
      </v-container>
      <model-document-step v-if="trainingType === 'documents'" :model="model" />
      <model-repository-step
        v-if="trainingType === 'repositories'"
        :model="model"
      />
      <model-keywords-step v-if="trainingType === 'keywords'" :model="model" />
      <model-project-step v-if="trainingType === 'project'" :model="model" />
    </v-card>
  </v-timeline-item>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import {
  ModelProjectStep,
  ModelDocumentStep,
  ModelRepositoryStep,
  ModelKeywordsStep,
} from "./steps";

/**
 * Displays inputs for training a model.
 */
export default Vue.extend({
  name: "ModelTrainingCreator",
  components: {
    ModelKeywordsStep,
    ModelRepositoryStep,
    ModelDocumentStep,
    ModelProjectStep,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      addOpen: false,
      trainingOptions: ["documents", "repositories", "keywords", "project"],
      trainingType: "documents",
    };
  },
});
</script>

<style scoped lang="scss"></style>

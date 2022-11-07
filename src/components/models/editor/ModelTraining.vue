<template>
  <v-container>
    <v-timeline dense>
      <model-training-step
        v-for="(step, idx) of steps"
        :key="idx"
        :step="step"
      />
      <model-training-creator :model="model" />
    </v-timeline>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel, TrainingStepModel } from "@/types";
import ModelTrainingStep from "./ModelTrainingStep.vue";
import ModelTrainingCreator from "./ModelTrainingCreator.vue";

const exampleSteps = [
  {
    type: "document",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "Completed",
    keywords: [],
    documents: [
      {
        name: "BOSCH Automotive Handbook.pdf",
        url: "https://path-to-gcp-bucket-file",
      },
    ],
    repositories: [],
    projects: [],
  },
  {
    type: "repository",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "Completed",
    keywords: [],
    documents: [],
    repositories: [
      {
        name: "organization/my-project",
        url: "https://path-to-git-hub-repo",
      },
    ],
    projects: [],
  },
  {
    type: "project",
    updatedAt: new Date(Date.now()).toISOString(),
    status: "In Progress",
    keywords: [],
    documents: [],
    repositories: [],
    projects: [
      {
        id: "123",
        name: "My Project",
        levels: [
          {
            source: "Designs",
            target: "Designs",
          },
          {
            source: "Designs",
            target: "Requirements",
          },
        ],
      },
    ],
  },
];

/**
 * Displays logs of the model's training process,
 * and allows for further model training.
 */
export default Vue.extend({
  name: "ModelTraining",
  components: {
    ModelTrainingCreator,
    ModelTrainingStep,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  computed: {
    steps(): TrainingStepModel[] {
      return [];
    },
  },
});
</script>

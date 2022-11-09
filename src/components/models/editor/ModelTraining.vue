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

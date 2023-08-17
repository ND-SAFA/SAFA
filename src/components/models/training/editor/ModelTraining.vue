<template>
  <q-timeline dense>
    <q-timeline-entry
      v-if="steps.length === 0"
      :subtitle="baseTimestamp"
      title="Model Training"
    >
      <typography
        value="This model has not yet been trained. To add a new training step, click the button below."
      />
    </q-timeline-entry>
    <model-training-step v-for="(step, idx) of steps" :key="idx" :step="step" />
    <model-training-creator :model="model" />
  </q-timeline>
</template>

<script lang="ts">
/**
 * Displays logs of the model's training process,
 * and allows for further model training.
 */
export default {
  name: "ModelTraining",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { GenerationModelProps } from "@/types";
import {
  ENABLED_FEATURES,
  EXAMPLE_TRAINING_STEPS,
  timestampToDisplay,
} from "@/util";
import { Typography } from "@/components/common";
import ModelTrainingStep from "./ModelTrainingStep.vue";
import ModelTrainingCreator from "./ModelTrainingCreator.vue";

const props = defineProps<GenerationModelProps>();

const baseTimestamp = timestampToDisplay(new Date(Date.now()).toISOString());

const steps = computed(() =>
  ENABLED_FEATURES.EXAMPLE_TRAINING_STEPS
    ? EXAMPLE_TRAINING_STEPS
    : props.model.steps || []
);
</script>

<template>
  <v-container>
    <v-timeline dense>
      <v-timeline-item small color="accent" v-if="steps.length === 0">
        <v-alert outlined border="left" color="accent">
          <typography
            value="This model has not yet been trained. To add a new training step, click the button below."
          />
        </v-alert>
      </v-timeline-item>
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
import { GenerationModelSchema, TrainingStepSchema } from "@/types";
import { ENABLED_FEATURES, EXAMPLE_TRAINING_STEPS } from "@/util";
import { Typography } from "@/components/common";
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
    Typography,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModelSchema>,
      required: true,
    },
  },
  computed: {
    /**
     * @return The logged steps of model training.
     */
    steps(): TrainingStepSchema[] {
      return ENABLED_FEATURES.EXAMPLE_TRAINING_STEPS
        ? EXAMPLE_TRAINING_STEPS
        : this.model.steps || [];
    },
  },
});
</script>

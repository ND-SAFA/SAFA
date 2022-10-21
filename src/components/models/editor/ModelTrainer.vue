<template>
  <generic-stepper v-model="step" :steps="steps" minimal hide-continue>
    <template v-slot:items>
      <v-stepper-content step="1">
        <model-keywords-step :model="model" />
      </v-stepper-content>
      <v-stepper-content step="2">
        <model-pre-training-step :model="model" />
      </v-stepper-content>
      <v-stepper-content step="3">
        <model-training-step :model="model" />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { GenericStepper } from "@/components/common";
import {
  ModelKeywordsStep,
  ModelPreTrainingStep,
  ModelTrainingStep,
} from "./steps";

/**
 * A stepper for training a trace generation model.
 */
export default Vue.extend({
  name: "ModelTrainer",
  components: {
    ModelKeywordsStep,
    ModelPreTrainingStep,
    ModelTrainingStep,
    GenericStepper,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      step: 1,
      steps: [
        ["Keywords & Documents", true],
        ["Pre-Training Materials", true],
        ["Model Training", true],
      ],
    };
  },
  computed: {},
  methods: {},
});
</script>

<template>
  <v-container>
    <v-stepper v-model="currentStep" alt-labels>
      <v-stepper-header>
        <template v-for="(stepName, stepIndex) in stepNames">
          <v-stepper-step
            :complete="currentStep > stepIndex + 1"
            :step="stepIndex + 1"
            :key="stepIndex"
          >
            {{ stepName }}
          </v-stepper-step>
          <v-divider
            :key="`${stepName}-divider`"
            v-if="stepIndex < stepNames.length - 1"
          />
        </template>
      </v-stepper-header>

      <v-stepper-items>
        <slot name="items" />
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

const SELECT_PROJECT_DEFAULT_NAME = "Select a Project";
const SELECT_VERSION_DEFAULT_NAME = "Select a Version";

export default Vue.extend({
  name: "generic-stepper",
  data() {
    return {
      currentSteps: [SELECT_PROJECT_DEFAULT_NAME, SELECT_VERSION_DEFAULT_NAME],
    };
  },
  props: {
    stepNames: {
      type: Array as PropType<Array<string>>,
      required: true,
    },
    value: {
      // current step number
      type: Number,
      required: true,
    },
  },
  computed: {
    currentStep: {
      get(): number {
        return this.value;
      },
      set(value: number): void {
        this.$emit("input", value);
      },
    },
  },
});
</script>

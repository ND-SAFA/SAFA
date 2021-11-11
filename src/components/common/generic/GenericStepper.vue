<template>
  <v-container>
    <v-card outlined elevation="1">
      <v-row>
        <v-stepper v-model="currentStep" style="width: 100%" alt-labels>
          <v-stepper-header>
            <template v-for="(stepName, stepIndex) in stepNames">
              <v-stepper-step
                :complete="currentStep > stepIndex + 1"
                :step="stepIndex + 1"
                :key="stepIndex"
                :editable="currentStep > stepIndex"
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
            <v-container>
              <v-btn
                :disabled="!isStepDone"
                @click="onStepForward"
                :color="currentStep === numberOfSteps ? 'secondary' : 'primary'"
              >
                {{ currentStep === numberOfSteps ? "Submit" : "Continue" }}
              </v-btn>
              <v-btn
                text
                @click="onStepBack"
                :disabled="currentStep === 1"
                color="primary"
              >
                Go Back
              </v-btn>
            </v-container>
          </v-stepper-items>
        </v-stepper>
      </v-row>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

export default Vue.extend({
  name: "generic-stepper",
  props: {
    value: {
      // current step number
      type: Number,
      required: true,
    },
    steps: {
      type: Array as PropType<Array<[string, boolean]>>,
      required: true,
      default: () => [] as [string, boolean][],
    },
  },
  methods: {
    onStepBack(): void {
      this.currentStep--;
    },
    onStepForward(): void {
      if (this.currentStep >= this.numberOfSteps) {
        this.$emit("onSubmit");
      } else {
        this.currentStep++;
      }
    },
  },
  computed: {
    isStepDone(): boolean {
      return this.steps[this.value - 1][1];
    },
    numberOfSteps(): number {
      return this.steps.length;
    },
    stepNames(): string[] {
      return this.steps.map((s) => s[0]);
    },
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

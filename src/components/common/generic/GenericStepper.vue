<template>
  <v-container>
    <v-row>
      <v-stepper v-model="currentStep" style="width: 100%" alt-labels>
        <v-container>
          <v-row>
            <v-col cols="1" align-self="center">
              <v-row justify="center">
                <v-btn
                  v-show="currentStep > 1"
                  @click="onStepBack"
                  fab
                  icon
                  outlined
                  small
                  color="primary"
                >
                  <v-icon id="upload-button">mdi-chevron-left</v-icon>
                </v-btn>
              </v-row>
            </v-col>
            <v-col cols="10">
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
            </v-col>
            <v-col cols="1" align-self="center">
              <v-row justify="center">
                <v-btn
                  v-if="isStepDone"
                  @click="onStepForward"
                  fab
                  outlined
                  icon
                  small
                  :color="
                    currentStep === numberOfSteps ? 'secondary' : 'primary'
                  "
                >
                  <v-icon id="upload-button">{{
                    currentStep === numberOfSteps
                      ? "mdi-check"
                      : "mdi-chevron-right"
                  }}</v-icon>
                </v-btn>
              </v-row>
            </v-col>
          </v-row>
        </v-container>

        <v-stepper-items>
          <slot name="items" />
        </v-stepper-items>
      </v-stepper>
    </v-row>
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
      if (this.currentStep === this.numberOfSteps) {
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

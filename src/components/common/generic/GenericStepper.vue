<template>
  <v-container>
    <v-row>
      <v-stepper v-model="currentStep" style="width: 100%">
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
    </v-row>
    <v-row class="mt-5">
      <v-container class="ma-0 pa-0">
        <v-row class="ma-0">
          <v-col cols="4" align-self="center">
            <v-row>
              <v-btn
                v-if="currentStep > 1"
                @click="onStepBack"
                fab
                small
                color="primary"
              >
                <v-icon id="upload-button">mdi-arrow-left</v-icon>
              </v-btn>
            </v-row>
          </v-col>
          <v-col cols="4">
            <slot name="actions:main" />
          </v-col>
          <v-col cols="4" align-self="center">
            <v-row justify="end">
              <v-btn
                v-if="isStepDone"
                @click="onStepForward"
                fab
                small
                :color="currentStep === numberOfSteps ? 'secondary' : 'primary'"
              >
                <v-icon id="upload-button">{{
                  currentStep === numberOfSteps
                    ? "mdi-check"
                    : "mdi-arrow-right"
                }}</v-icon>
              </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
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

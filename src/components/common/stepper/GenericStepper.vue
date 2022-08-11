<template>
  <v-container>
    <v-card :outlined="!minimal" :style="minimal ? 'box-shadow: none' : ''">
      <v-row>
        <v-stepper
          v-model="currentStep"
          class="full-width"
          :alt-labels="!minimal"
          :elevation="minimal ? 0 : 1"
        >
          <v-stepper-header :style="minimal ? 'box-shadow: none' : ''">
            <template v-for="(stepName, stepIndex) in stepNames">
              <v-stepper-step
                :complete="currentStep > stepIndex + 1"
                :step="stepIndex + 1"
                :key="stepIndex"
                :editable="currentStep > stepIndex"
              >
                <typography :value="stepName" class="width-max" el="div" />
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
                color="primary"
                :outlined="currentStep !== numberOfSteps"
                :disabled="!isStepDone"
                @click="onStepForward"
              >
                {{ currentStep === numberOfSteps ? submitText : "Continue" }}
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
import { Typography } from "@/components/common/display";

/**
 * Displays a generic stepper.
 *
 * @emits-1 `input` (number) - On input change.
 * @emits-2 `submit` - On submit.
 */
export default Vue.extend({
  name: "GenericStepper",
  components: { Typography },
  props: {
    value: {
      // Current step number
      type: Number,
      required: true,
    },
    steps: {
      type: Array as PropType<Array<[string, boolean]>>,
      required: true,
      default: () => [] as [string, boolean][],
    },
    submitText: {
      type: String,
      default: "Submit",
    },
    minimal: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    /**
     * Moves one step backward.
     */
    onStepBack(): void {
      this.currentStep--;
    },
    /**
     * Moves one step forward, or submits if on the last step.
     */
    onStepForward(): void {
      if (this.currentStep >= this.numberOfSteps) {
        this.$emit("submit");
      } else {
        this.currentStep++;
      }
    },
  },
  computed: {
    /**
     * @return Whether the current step is done.
     */
    isStepDone(): boolean {
      return this.steps[this.value - 1][1];
    },
    /**
     * @return WThe total number of steps.
     */
    numberOfSteps(): number {
      return this.steps.length;
    },
    /**
     * @return All step names.
     */
    stepNames(): string[] {
      return this.steps.map((s) => s[0]);
    },
    /**
     * @return The current step, which emits its value when changed.
     */
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

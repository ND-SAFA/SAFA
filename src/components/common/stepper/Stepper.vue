<template>
  <v-card
    :outlined="!minimal"
    :style="minimal ? 'box-shadow: none' : ''"
    :class="minimal ? '' : 'primary-border'"
  >
    <v-stepper
      v-model="currentStep"
      class="full-width transparent-bg"
      :alt-labels="!minimal"
      :elevation="minimal ? 0 : 1"
    >
      <v-stepper-header :style="minimal ? 'box-shadow: none' : ''">
        <template v-for="(stepName, stepIndex) in stepNames" :key="stepIndex">
          <v-stepper-step
            :complete="currentStep > stepIndex + 1"
            :step="stepIndex + 1"
            :editable="steps[stepIndex][1]"
          >
            <typography :value="stepName" class="width-max" el="div" />
          </v-stepper-step>
          <v-divider v-if="stepIndex < stepNames.length - 1" />
        </template>
      </v-stepper-header>

      <v-stepper-items>
        <slot name="items" />
        <v-container v-if="!hideContinue">
          <v-btn
            color="primary"
            :outlined="currentStep !== steps.length"
            :disabled="!isStepDone"
            data-cy="button-stepper-continue"
            @click="onStepForward"
          >
            {{ continueText }}
          </v-btn>
          <v-btn
            text
            :disabled="currentStep === 1"
            color="primary"
            data-cy="button-stepper-back"
            @click="onStepBack"
          >
            Go Back
          </v-btn>
        </v-container>
      </v-stepper-items>
    </v-stepper>
  </v-card>
</template>

<script lang="ts">
/**
 * Displays a generic stepper.
 */
export default {
  name: "Stepper",
};
</script>

<script setup lang="ts">
import { withDefaults, defineProps, defineEmits, computed } from "vue";
import { useVModel } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = withDefaults(
  defineProps<{
    /**
     * The current step number.
     */
    modelValue: number;
    steps: [string, boolean][];
    submitText?: string;
    minimal?: boolean;
    hideContinue?: boolean;
  }>(),
  {
    submitText: "Submit",
  }
);

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const isStepDone = computed(() => props.steps[props.modelValue - 1][1]);
const stepNames = computed(() => props.steps.map((s) => s[0]));
const currentStep = useVModel(props, "modelValue");
const continueText = computed(() =>
  currentStep.value === props.steps.length ? props.submitText : "Continue"
);

/**
 * Moves one step backward.
 */
function onStepBack(): void {
  currentStep.value--;
}

/**
 * Moves one step forward, or submits if on the last step.
 */
function onStepForward(): void {
  if (currentStep.value >= props.steps.length) {
    emit("submit");
  } else {
    currentStep.value++;
  }
}
</script>

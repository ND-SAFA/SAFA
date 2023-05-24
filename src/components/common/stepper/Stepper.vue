<template>
  <q-stepper
    v-model="currentStep"
    flat
    animated
    :class="className"
    header-nav
    :alternative-labels="minimal"
  >
    <q-step
      v-for="(step, idx) in props.steps"
      :key="step.title"
      :name="idx + 1"
      :title="step.title"
      :done="step.done"
      :caption="step.caption"
      :header-nav="step.done"
    >
      <slot :name="idx + 1" />
    </q-step>

    <template v-if="!props.hideActions" #navigation>
      <q-stepper-navigation class="q-mt-sm">
        <slot name="actions" />
        <flex-box full-width align="end">
          <text-button
            color="primary"
            :outlined="currentStep !== steps.length"
            :disabled="!isStepDone"
            data-cy="button-stepper-continue"
            :label="continueText"
            @click="onStepForward"
          />
          <text-button
            text
            color="primary"
            :disabled="currentStep === 1"
            data-cy="button-stepper-back"
            label="Back"
            class="q-ml-sm"
            @click="onStepBack"
          />
        </flex-box>
      </q-stepper-navigation>
    </template>
  </q-stepper>
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
import { computed } from "vue";
import { StepperProps } from "@/types";
import { useVModel } from "@/hooks";
import { TextButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/display";

const props = defineProps<StepperProps>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const currentStep = useVModel(props, "modelValue");

const isStepDone = computed(() => props.steps[props.modelValue - 1].done);
const continueText = computed(() =>
  currentStep.value === props.steps.length ? "Submit" : "Continue"
);
const className = computed(() =>
  props.denseLabels
    ? "full-width bg-transparent stepper-minimal"
    : "full-width bg-transparent"
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

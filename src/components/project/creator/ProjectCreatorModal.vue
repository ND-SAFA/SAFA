<template>
  <GenericStepperModal
    v-model="currentStep"
    title="Create a New Project"
    size="l"
    :steps="steps"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @onClose="onClose"
    @onReset="clearData"
    @onSubmit="$emit('onSubmit')"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container class="pa-10">
          <ProjectCreator
            v-bind:name.sync="name"
            v-bind:description.sync="description"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-container class="pa-10">
          <ArtifactFileUploader
            @onIsValid="setStepIsValid(1, true)"
            @onIsInvalid="setStepIsValid(1, false)"
          />
        </v-container>
      </v-stepper-content>
    </template>

    <template v-slot:action:main>
      <slot name="action:main" />
    </template>
  </GenericStepperModal>
</template>

<script lang="ts">
import Vue from "vue";
import GenericStepperModal from "@/components/common/generic/GenericStepperModal.vue";
import type { StepState } from "@/types/common-components";
import ProjectCreator from "@/components/project/shared/ProjectIdentifierInput.vue";
import ArtifactFileUploader from "@/components/project/creator/ArtifactFileUploader.vue";

export default Vue.extend({
  name: "project-creator-modal",
  components: {
    GenericStepperModal,
    ProjectCreator,
    ArtifactFileUploader,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      steps: [
        ["Name Project", false],
        ["Select Artifact Files", false],
        ["Project TIM", false],
      ] as StepState[],
      name: "",
      description: "",
      currentStep: 2,
      isLoading: false,
    };
  },
  methods: {
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      Vue.set(this.steps, stepIndex, [this.steps[stepIndex][0], isValid]);
    },
    clearData() {
      this.currentStep = 1;
      this.isLoading = false;
    },
    onClose() {
      this.$emit("onClose");
    },
  },
  computed: {
    totalSteps(): number {
      return this.steps.length;
    },
    combinedState(): string {
      return this.name + this.description;
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
    currentStep(nextStep: number): void {
      switch (nextStep) {
        case 2:
          Vue.set(this.steps, 0, [this.name, true]);
          break;
        default:
          break;
      }
    },
    name(): void {
      const isFirstStepValid = this.name !== "";
      Vue.set(this.steps, 0, [this.name, isFirstStepValid]);
    },
  },
});
</script>

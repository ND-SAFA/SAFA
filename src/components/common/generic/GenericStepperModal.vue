<template>
  <GenericModal
    :title="title"
    :isOpen="isOpen"
    :isLoading="isLoading"
    :size="size"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <GenericStepper
        v-model="currentStep"
        :isOpen="isOpen"
        :stepNames="stepNames"
        @onReset="$emit('onReset')"
      >
        <template v-slot:items>
          <slot name="items" />
        </template>
      </GenericStepper>
    </template>
    <template v-slot:actions>
      <v-container class="ma-0 pa-0">
        <v-row class="ma-0">
          <v-col cols="4" align-self="center">
            <v-btn v-if="currentStep > 1" @click="onStepBack" fab small>
              <v-icon id="upload-button">mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4">
            <slot name="action:main" />
          </v-col>
          <v-col cols="4" align-self="center">
            <v-row justify="end">
              <v-btn
                v-if="isStepDone"
                @click="onStepForward"
                fab
                small
                :color="currentStep === numberOfSteps ? 'secondary' : undefined"
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
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import { ModalSize } from "@/types";
import GenericStepper from "@/components/common/generic/GenericStepper.vue";

export default Vue.extend({
  name: "generic-stepper-modal",
  components: {
    GenericModal,
    GenericStepper,
  },
  props: {
    value: {
      //curent step
      type: Number,
      required: true,
      default: 1,
    },
    steps: {
      type: Array as PropType<Array<[string, boolean]>>,
      required: true,
      default: () => [] as [string, boolean][],
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    size: {
      type: String as PropType<ModalSize>,
      required: false,
      default: "m",
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
    currentStep: {
      get(): number {
        return this.value;
      },
      set(newStep: number): void {
        this.$emit("input", newStep);
      },
    },
    stepNames(): string[] {
      return this.steps.map((step) => step[0]);
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.$emit("onReset");
      }
    },
  },
});
</script>

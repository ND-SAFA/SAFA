<template>
  <GenericModal
    :title="title"
    :isOpen="isOpen"
    :isLoading="isLoading"
    :size="size"
    :actionsHeight="0"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <GenericStepper
        v-model="currentStep"
        :steps="steps"
        @onReset="$emit('onReset')"
        @onSubmit="$emit('onSubmit')"
      >
        <template v-slot:items>
          <slot name="items" />
        </template>
      </GenericStepper>
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
  computed: {
    currentStep: {
      get(): number {
        return this.value;
      },
      set(newStep: number): void {
        this.$emit("input", newStep);
      },
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

<template>
  <generic-modal
    :title="title"
    :is-open="isOpen"
    :is-loading="isLoading"
    :size="size"
    :actions-height="0"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <generic-stepper
        v-model="currentStep"
        :steps="steps"
        @submit="$emit('submit')"
      >
        <template v-slot:items>
          <slot name="items" />
        </template>
      </generic-stepper>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ModalSize } from "@/types";
import GenericModal from "./GenericModal.vue";
import GenericStepper from "./GenericStepper.vue";

/**
 * Displays a generic stepper modal.
 *
 * @emits-1 `input` (number) - On input change.
 * @emits-2 `reset` - On reset.
 * @emits-3 `close` - On close.
 * @emits-4 `submit` - On submit.
 */
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
        this.$emit("reset");
      }
    },
  },
});
</script>

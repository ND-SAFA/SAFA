<template>
  <v-dialog
    :value="isOpen"
    :width="`${width}px`"
    :retain-focus="false"
    persistent
  >
    <v-card :class="`modal-${size}`" :data-cy="dataCy">
      <v-card-title class="primary">
        <generic-modal-title :title="title" @close="$emit('close')" />
      </v-card-title>

      <v-card-text>
        <slot name="body" />
      </v-card-text>

      <v-divider />

      <v-progress-linear v-if="isLoading" indeterminate color="secondary" />

      <v-card-actions
        v-if="actionsHeight > 0"
        dense
        :style="`height: ${actionsHeight}px`"
      >
        <slot name="actions" />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ModalSize } from "@/types";
import GenericModalTitle from "./GenericModalTitle.vue";

/**
 * Displays a generic modal.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "generic-modal",
  components: {
    GenericModalTitle,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    actionsHeight: {
      type: Number,
      required: false,
      default: 50,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String as PropType<ModalSize>,
      required: false,
      default: "m",
    },
    dataCy: String,
  },
  computed: {
    /**
     * @return The modal width.
     */
    width(): number {
      switch (this.size) {
        case "xxs":
          return 250;
        case "xs":
          return 300;
        case "s":
          return 400;
        case "m":
          return 600;
        case "l":
          return 800;
        default:
          return 400;
      }
    },
  },
});
</script>

<style scoped>
html {
  overflow: hidden !important;
}
</style>

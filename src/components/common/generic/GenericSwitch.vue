<template>
  <v-switch v-model="switchValue" :label="label" class="generic-switch" />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a generic switch.
 *
 * @emits `input` (boolean) - On input change.
 */
export default Vue.extend({
  name: "generic-switch",
  props: {
    label: {
      type: String,
      required: true,
    },
    value: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    switchValue: {
      get(): boolean {
        return this.value;
      },
      set(isOn: boolean): void {
        this.$emit("input", isOn);
      },
    },
  },
});
</script>

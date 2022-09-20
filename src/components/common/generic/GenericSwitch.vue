<template>
  <v-switch inset v-model="switchValue" :label="label" class="mr-2" />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a generic switch.
 *
 * @emits `input` (boolean) - On input change.
 */
export default Vue.extend({
  name: "GenericSwitch",
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
    /**
     * @return The current value, and emits the value when changed.
     */
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

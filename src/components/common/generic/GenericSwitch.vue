<template>
  <v-switch v-model="switchValue" :label="label" class="generic-switch" />
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
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

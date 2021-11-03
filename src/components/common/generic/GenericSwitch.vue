<template>
  <v-row>
    <v-col align-self="center" cols="9">{{ label }}</v-col>
    <v-col align-self="center" cols="3"
      ><v-switch v-model="switchValue" />
    </v-col>
  </v-row>
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

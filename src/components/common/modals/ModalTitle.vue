<template>
  <v-row justify="space-between">
    <label>{{ title }}</label>
    <v-btn @click="$emit('onClose')" icon>
      <v-icon id="close-button">mdi-close</v-icon>
    </v-btn>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    title: {
      type: String,
      required: true,
    },
  },
});
</script>

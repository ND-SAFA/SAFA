<template>
  <v-row justify="center">
    <v-btn
      small
      text
      color="error"
      outlined
      @click="$emit('close-all')"
      class="ma-1"
    >
      <v-icon>mdi-arrow-collapse-all</v-icon>
    </v-btn>
    <v-btn
      small
      text
      color="primary"
      outlined
      @click="$emit('open-all')"
      class="ma-1"
    >
      <v-icon>mdi-arrow-expand-all</v-icon>
    </v-btn>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays section controls.
 *
 * @emits `open-all` - On left button click.
 * @emits `close-all` - On right button click.
 */
export default Vue.extend({
  name: "section-controls",
});
</script>

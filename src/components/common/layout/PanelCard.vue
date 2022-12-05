<template>
  <v-card outlined class="pa-2 mb-4 primary lighten-4 overflow-hidden">
    <slot />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a card that contains panel content.
 */
export default Vue.extend({
  name: "PanelCard",
});
</script>

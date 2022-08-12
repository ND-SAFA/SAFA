<template>
  <v-container>
    <v-data-table show-group-by show-expand fixed-header> </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",
});
</script>

<style scoped></style>

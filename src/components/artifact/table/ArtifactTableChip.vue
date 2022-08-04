<template>
  <v-tooltip bottom z-index="12" :disabled="text.length < 10">
    <template v-slot:activator="{ on, attrs }">
      <v-chip
        v-on="on"
        v-bind="attrs"
        small
        class="text-body-1 mr-1"
        style="max-width: 200px"
      >
        <span class="text-ellipsis">{{ text }}</span>
      </v-chip>
    </template>
    <span>{{ text }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Renders a chip on an artifact table row.
 */
export default Vue.extend({
  name: "ArtifactTableChip",
  props: {
    text: String,
  },
});
</script>

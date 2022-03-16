<template>
  <v-chip small class="text-body-1 mr-1" style="max-width: 80px">
    <span class="text-ellipsis">{{ text }}</span>
  </v-chip>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * ArtifactTableChip
 */
export default Vue.extend({
  name: "ArtifactTableChip",
  props: {
    text: String,
  },
});
</script>

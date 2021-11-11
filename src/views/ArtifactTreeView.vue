<template>
  <v-container fluid>
    <v-row justify="center" class="ma-1">
      <VersionLabel />
    </v-row>
    <v-row class="ma-1">
      <ArtifactTree />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactTree, VersionLabel } from "@/components/artifact-tree-view";

export default Vue.extend({
  name: "Home",
  components: {
    ArtifactTree,
    VersionLabel,
  },
});
</script>

<template>
  <private-page>
    <template v-slot:page>
      <v-container fluid>
        <v-row justify="center" class="ma-1">
          <VersionLabel />
        </v-row>
        <v-row class="ma-1">
          <ArtifactTree />
        </v-row>
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactTree, VersionLabel, PrivatePage } from "@/components";

/**
 * Displays the artifact tree of the current project with a label
 * above it containing the current project and version.
 */
export default Vue.extend({
  name: "Home",
  components: {
    PrivatePage,
    ArtifactTree,
    VersionLabel,
  },
});
</script>

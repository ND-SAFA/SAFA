<template>
  <v-container>
    <h1 class="text-h4 my-2">Trace Directions</h1>
    <div v-for="entry in artifactDirections" :key="entry.type">
      <h2 class="text-h5 mb-2">{{ entry.label }}</h2>
      <v-autocomplete
        filled
        multiple
        chips
        deletable-chips
        v-model="entry.allowedTypes"
        :items="artifactTypes"
        @change="onChange(entry.type, $event)"
      />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { linkDirectionsModule, projectModule } from "@/store";
import { capitalizeSentence } from "@/util";
import { LabeledArtifactDirection } from "@/types";

export default Vue.extend({
  name: "trace-link-direction-tab",
  data() {
    return {
      artifactTypes: [] as string[],
      artifactDirections: [] as LabeledArtifactDirection[],
    };
  },
  mounted() {
    this.artifactTypes = linkDirectionsModule.artifactTypes;

    this.artifactDirections = Object.entries(
      linkDirectionsModule.linkDirections
    ).map(([type, allowedTypes]) => ({
      type,
      allowedTypes,
      label: capitalizeSentence(type),
    }));
  },
  methods: {
    onChange(type: string, allowedTypes: string[]) {
      linkDirectionsModule.updateLinkDirections({
        type,
        allowedTypes,
      });
    },
  },
});
</script>

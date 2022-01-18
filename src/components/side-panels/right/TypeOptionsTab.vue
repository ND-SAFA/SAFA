<template>
  <v-container>
    <h1 class="text-h4 my-2">Type Options</h1>
    <div v-for="entry in artifactDirections" :key="entry.type">
      <h2 class="text-h5 mb-2">{{ entry.label }}</h2>
      <v-autocomplete
        filled
        multiple
        chips
        deletable-chips
        v-model="entry.allowedTypes"
        :items="artifactTypes"
        :label="entry.label + ' Trace To'"
        @change="onDirectionChange(entry)"
      />
      <v-autocomplete
        filled
        v-model="entry.icon"
        :items="icons"
        :label="entry.label + ' Icon'"
        :append-icon="entry.icon"
        @change="onIconChange(entry)"
      />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LabeledArtifactDirection } from "@/types";
import { getArtifactTypePrintName } from "@/util";
import { typeOptionsModule } from "@/store";

export default Vue.extend({
  name: "trace-link-direction-tab",
  data() {
    return {
      artifactTypes: [] as string[],
      artifactDirections: [] as LabeledArtifactDirection[],
    };
  },
  mounted() {
    this.artifactTypes = typeOptionsModule.artifactTypes;

    this.artifactDirections = Object.entries(
      typeOptionsModule.linkDirections
    ).map(([type, allowedTypes]) => ({
      type,
      allowedTypes,
      label: getArtifactTypePrintName(type),
      icon: typeOptionsModule.getArtifactTypeIcon(type),
    }));
  },
  computed: {
    icons() {
      return Object.values(typeOptionsModule.allArtifactTypeIcons);
    },
  },
  methods: {
    onDirectionChange(entry: LabeledArtifactDirection) {
      typeOptionsModule.updateLinkDirections(entry);
    },
    onIconChange(entry: LabeledArtifactDirection) {
      typeOptionsModule.updateArtifactIcon(entry);
    },
  },
});
</script>

<style>
.v-autocomplete.v-select--is-menu-active .v-input__icon--append .v-icon {
  transform: none !important;
}
</style>

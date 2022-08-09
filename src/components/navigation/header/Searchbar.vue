<template>
  <v-autocomplete
    outlined
    dense
    hide-details
    dark
    clearable
    label="Search artifacts"
    color="secondary"
    v-model="value"
    :items="artifacts"
    item-text="name"
    item-value="id"
    class="mx-1 mt-1"
    style="min-width: 200px"
    :filter="filterArtifacts"
  >
    <template v-slot:item="{ item }">
      <generic-artifact-body-display display-title :artifact="item" />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact } from "@/types";
import {
  artifactModule,
  artifactSelectionModule,
  viewportModule,
} from "@/store";
import { GenericArtifactBodyDisplay } from "@/components/common";
import { filterArtifacts } from "@/util";

/**
 * Artifact search bar.
 */
export default Vue.extend({
  name: "Searchbar",
  components: {
    GenericArtifactBodyDisplay,
  },
  methods: {
    filterArtifacts,
  },
  computed: {
    /**
     * @return The artifacts to select from.
     */
    artifacts(): Artifact[] {
      return artifactModule.artifacts;
    },
    value: {
      get() {
        return artifactSelectionModule.getSelectedArtifactId;
      },
      set(artifactId: string | null) {
        if (artifactId) {
          viewportModule.viewArtifactSubtree(artifactId);
        } else {
          artifactSelectionModule.clearSelections();
        }
      },
    },
  },
});
</script>

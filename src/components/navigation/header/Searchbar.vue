<template>
  <v-form style="min-width: 200px; width: 30vw">
    <v-autocomplete
      outlined
      dense
      hide-details
      dark
      clearable
      label="Search Artifacts"
      color="secondary"
      v-model="value"
      :items="artifacts"
      :search-input.sync="queryText"
      item-text="name"
      item-value="id"
      class="mx-1 mt-1"
      append-icon="mdi-magnify"
      :filter="filterArtifacts"
    >
      <template v-slot:prepend-item>
        <flex-box x="3">
          <v-spacer />
          <typography align="end" variant="caption" :value="matchText" />
        </flex-box>
      </template>
      <template v-slot:item="{ item }">
        <generic-artifact-body-display display-title :artifact="item" />
      </template>
    </v-autocomplete>
  </v-form>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactSearchItem } from "@/types";
import {
  artifactModule,
  artifactSelectionModule,
  viewportModule,
} from "@/store";
import { GenericArtifactBodyDisplay, Typography } from "@/components/common";
import { filterArtifacts, getArtifactTypePrintName } from "@/util";
import FlexBox from "@/components/common/display/FlexBox.vue";

/**
 * Artifact search bar.
 */
export default Vue.extend({
  name: "Searchbar",
  components: {
    FlexBox,
    Typography,
    GenericArtifactBodyDisplay,
  },
  data() {
    return {
      queryText: "" as string | null,
    };
  },
  methods: {
    /**
     * Filters what artifacts are currently visible.
     * @param artifact
     * @param queryText
     */
    filterArtifacts(artifact: ArtifactSearchItem, queryText: string | null) {
      if (!queryText) {
        return true;
      } else if ("header" in artifact || "divider" in artifact) {
        return false;
      } else {
        return filterArtifacts(artifact, queryText);
      }
    },
  },
  computed: {
    /**
     * Returns the display text for how many matches there are.
     */
    matchText(): string {
      if (!this.queryText) return "";

      const count = artifactModule.artifacts.filter((artifact) =>
        filterArtifacts(artifact, this.queryText || "")
      ).length;

      return count === 1 ? "1 Match" : `${count} Matches`;
    },
    /**
     * @return The artifacts to select from.
     */
    artifacts(): ArtifactSearchItem[] {
      return Object.entries(artifactModule.getArtifactsByType)
        .map(([type, artifacts]) => [
          { header: getArtifactTypePrintName(type) },
          ...artifacts,
        ])
        .reduce((acc, cur) => [...acc, ...cur], []);
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

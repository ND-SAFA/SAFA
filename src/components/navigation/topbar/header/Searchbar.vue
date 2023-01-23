<template>
  <v-form style="min-width: 200px; width: 30vw">
    <v-autocomplete
      outlined
      dense
      hide-details
      dark
      clearable
      label="Search Artifacts"
      color="accent"
      v-model="value"
      :items="artifacts"
      :search-input.sync="queryText"
      item-text="name"
      item-value="id"
      class="mx-1 mt-1 nav-input"
      :filter="filterArtifacts"
      data-cy="input-artifact-search-nav"
    >
      <template v-slot:append>
        <v-icon color="accent" class="input-no-icon-rotate">
          mdi-magnify
        </v-icon>
      </template>
      <template v-slot:prepend-item>
        <flex-box x="3">
          <v-spacer />
          <typography
            align="end"
            variant="caption"
            :value="matchText"
            data-cy="text-artifact-search-count"
          />
        </flex-box>
      </template>
      <template v-slot:item="{ item }">
        <artifact-body-display
          display-title
          :artifact="item"
          data-cy="text-artifact-search-item"
        />
      </template>
    </v-autocomplete>
  </v-form>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactSearchItem } from "@/types";
import { filterArtifacts, objectToArray } from "@/util";
import { typeOptionsStore, artifactStore, selectionStore } from "@/hooks";
import { ArtifactBodyDisplay, Typography, FlexBox } from "@/components/common";

/**
 * Artifact search bar.
 */
export default Vue.extend({
  name: "Searchbar",
  components: {
    FlexBox,
    Typography,
    ArtifactBodyDisplay,
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

      const count = artifactStore.currentArtifacts.filter((artifact) =>
        filterArtifacts(artifact, this.queryText || "")
      ).length;

      return count === 1 ? "1 Match" : `${count} Matches`;
    },
    /**
     * @return The artifacts to select from.
     */
    artifacts(): ArtifactSearchItem[] {
      return objectToArray(
        artifactStore.getArtifactsByType,
        ([type, artifacts]) => [
          { header: typeOptionsStore.getArtifactTypeDisplay(type) },
          ...artifacts,
        ]
      );
    },
    value: {
      get() {
        return selectionStore.selectedArtifact?.id;
      },
      set(artifactId: string | null) {
        if (artifactId) {
          selectionStore.viewArtifactSubtree(artifactId);
        } else {
          selectionStore.clearSelections();
        }
      },
    },
  },
});
</script>

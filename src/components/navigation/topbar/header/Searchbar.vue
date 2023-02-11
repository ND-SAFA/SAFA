<template>
  <v-form style="min-width: 200px; width: 30vw">
    <v-autocomplete
      v-model="value"
      v-model:search-input="queryText"
      variant="outlined"
      density="compact"
      hide-details
      clearable
      label="Search Artifacts"
      color="accent"
      :items="artifacts"
      item-text="name"
      item-value="id"
      class="mx-1 mt-1 nav-input"
      :filter="filter"
      data-cy="input-artifact-search-nav"
    >
      <template #prepend-inner>
        <v-icon color="accent" class="input-no-icon-rotate">
          mdi-magnify
        </v-icon>
      </template>
      <template #prepend-item>
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
      <template #item="{ item }">
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
/**
 * Artifact search bar.
 */
export default {
  name: "Searchbar",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactSearchItem } from "@/types";
import { filterArtifacts, objectToArray } from "@/util";
import { typeOptionsStore, artifactStore, selectionStore } from "@/hooks";
import { ArtifactBodyDisplay, Typography, FlexBox } from "@/components/common";

const queryText = ref<string | null>("");

/**
 * Filters what artifacts are currently visible.
 * @param artifact - The artifact item to filter.
 * @param queryText - The current query text.
 */
function filter(artifact: ArtifactSearchItem, queryText: string | null) {
  if (!queryText) {
    return true;
  } else if ("header" in artifact || "divider" in artifact) {
    return false;
  } else {
    return filterArtifacts(artifact, queryText);
  }
}

/**
 * Returns the display text for how many matches there are.
 */
const matchText = computed(() => {
  if (!queryText.value) return "";

  const count = artifactStore.currentArtifacts.filter((artifact) =>
    filter(artifact, queryText.value || "")
  ).length;

  return count === 1 ? "1 Match" : `${count} Matches`;
});

const artifacts = computed(() =>
  objectToArray(artifactStore.getArtifactsByType, ([type, artifacts]) => [
    { header: typeOptionsStore.getArtifactTypeDisplay(type) },
    ...artifacts,
  ])
);

const value = computed({
  get() {
    return selectionStore.selectedArtifact?.id;
  },
  set(artifactId: string | undefined) {
    if (artifactId) {
      selectionStore.viewArtifactSubtree(artifactId);
    } else {
      selectionStore.clearSelections();
    }
  },
});
</script>

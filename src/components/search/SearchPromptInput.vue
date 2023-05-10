<template>
  <q-select
    v-model="searchStore.searchItems"
    outlined
    use-input
    clearable
    multiple
    :label="searchStore.mode.placeholder"
    :options="searchOptions"
    :option-label="searchStore.artifactLikeMode ? 'name' : undefined"
    :option-value="searchStore.artifactLikeMode ? 'id' : undefined"
    input-debounce="0"
    class="nav-search-prompt"
    style="width: 600px; max-width: 40vw"
    @update:model-value="clearOptions"
    @filter="filterOptions"
  >
    <template #append>
      <icon variant="search" />
    </template>
    <template #before-options>
      <flex-box x="3" t="1" justify="end">
        <typography
          align="end"
          variant="caption"
          :value="matchText"
          data-cy="text-artifact-search-count"
        />
      </flex-box>
    </template>
    <template #option="{ opt, itemProps }">
      <search-option v-bind="itemProps" :option="opt" />
    </template>
    <template v-if="!searchStore.basicSearchMode" #no-option>
      <search-inputs @submit="handleProjectSearch" />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * Displays a search prompt that allows the user to search for artifacts.
 */
export default {
  name: "SearchPromptInput",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ArtifactSchema } from "@/types";
import { filterArtifacts } from "@/util";
import {
  artifactStore,
  searchStore,
  selectionStore,
  typeOptionsStore,
} from "@/hooks";
import { handleProjectSearch } from "@/api";
import { Typography, Icon, FlexBox } from "@/components/common";
import SearchOption from "./SearchOption.vue";
import SearchInputs from "./SearchInputs.vue";

const searchOptions = ref<ArtifactSchema[] | string[]>([]);

/**
 * Returns the display text for how many matches there are.
 */
const matchText = computed(() => {
  const count = searchOptions.value.length;

  return count === 1 ? "1 Match" : `${count} Matches`;
});

/**
 * Clears options if an item has been selected.
 */
function clearOptions(): void {
  searchOptions.value =
    searchStore.selectionCount > 0 ? [] : searchOptions.value;
}

/**
 * Filters the options based on the search text.
 * @param search - The search text.
 * @param update - A function called to update the options.
 */
function filterOptions(search: string, update: (fn: () => void) => void) {
  searchStore.searchText = search;

  if (search === "" || searchStore.selectionCount > 0) {
    update(() => (searchOptions.value = []));
  } else {
    update(() => {
      if (searchStore.artifactLikeMode) {
        searchOptions.value = artifactStore.currentArtifacts.filter(
          (artifact) => filterArtifacts(artifact, search)
        );
      } else if (searchStore.artifactTypeMode) {
        const lowercaseSearch = search.toLowerCase();

        searchOptions.value = typeOptionsStore.artifactTypes.filter((type) =>
          type.toLowerCase().includes(lowercaseSearch)
        );
      } else {
        searchOptions.value = [];
      }
    });
  }
}

/**
 * When the search changes in basic search mode,
 * highlight the selected artifact.
 */
watch(
  () => searchStore.searchItems,
  (artifacts: ArtifactSchema[] | string[] | null) => {
    if (!searchStore.basicSearchMode) return;

    if (
      !!artifacts &&
      artifacts.length === 1 &&
      typeof artifacts[0] === "object"
    ) {
      selectionStore.viewArtifactSubtree(artifacts[0].id);
    } else {
      selectionStore.clearSelections();
    }
  }
);
</script>

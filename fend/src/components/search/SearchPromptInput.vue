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
    class="nav-input nav-search-prompt nav-multi-input-right"
    menu-anchor="bottom middle"
    menu-self="top middle"
    data-cy="input-nav-artifact-search"
    @update:model-value="clearOptions"
    @filter="filterOptions"
    @keydown.enter="handleChat"
  >
    <template #append>
      <icon variant="search" />
    </template>
    <template #before-options>
      <flex-box l="2" y="2" justify="between" align="center">
        <typography
          variant="caption"
          :value="matchText"
          data-cy="text-artifact-search-count"
        />
        <type-buttons
          default-visible
          :hidden-types="hiddenTypes"
          @click="handleTypeChange"
        />
      </flex-box>
    </template>
    <template #option="{ opt, itemProps }">
      <search-option v-bind="itemProps" :option="opt" />
    </template>
    <template
      v-if="!searchStore.basicSearchMode && !searchStore.chatSearchMode"
      #no-option
    >
      <search-inputs @submit="searchApiStore.handleSearch" />
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
import { ArtifactSchema, ArtifactTypeSchema } from "@/types";
import { filterArtifacts } from "@/util";
import {
  artifactStore,
  chatApiStore,
  chatStore,
  layoutStore,
  searchApiStore,
  searchStore,
  selectionStore,
  timStore,
} from "@/hooks";
import { Typography, Icon, FlexBox, TypeButtons } from "@/components/common";
import SearchOption from "./SearchOption.vue";
import SearchInputs from "./SearchInputs.vue";

const searchOptions = ref<ArtifactSchema[] | string[]>([]);
const hiddenTypes = ref<string[]>([]);
const currentText = ref("");

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
  currentText.value = search;

  update(() => {
    if (
      searchStore.basicSearchMode ||
      (searchStore.artifactLikeMode && search !== "")
    ) {
      // Basic search always shows artifacts.
      // Artifact-like search only shows artifacts when there is search text.
      searchOptions.value = artifactStore.currentArtifacts.filter(
        (artifact) =>
          !hiddenTypes.value.includes(artifact.type) &&
          filterArtifacts(artifact, search)
      );
    } else if (search === "" || searchStore.selectionCount > 0) {
      // Non-basic search shows no artifacts when there is no search text.
      searchOptions.value = [];
    } else if (searchStore.artifactTypeMode) {
      // Artifact type search shows artifact types when there is search text.
      const lowercaseSearch = search.toLowerCase();

      searchOptions.value = timStore.typeNames.filter((type) =>
        type.toLowerCase().includes(lowercaseSearch)
      );
    } else {
      searchOptions.value = [];
    }
  });
}

/**
 * Toggles whether a type is visible in the artifact list.
 * @param option - The type to toggle.
 * @param allOptions - All possible types.
 */
function handleTypeChange(
  option: ArtifactTypeSchema,
  allOptions: ArtifactTypeSchema[]
): void {
  if (hiddenTypes.value.length === 0) {
    hiddenTypes.value = allOptions
      .map((type) => type.name)
      .filter((type) => type !== option.name);
  } else if (hiddenTypes.value.find((type) => type === option.name)) {
    hiddenTypes.value = hiddenTypes.value.filter(
      (type) => type !== option.name
    );
  } else {
    hiddenTypes.value.push(option.name);
  }

  if (hiddenTypes.value.length === allOptions.length) {
    hiddenTypes.value = [];
  }

  searchOptions.value = artifactStore.currentArtifacts.filter(
    (artifact) => !hiddenTypes.value.includes(artifact.type)
  );
}

/**
 * Handles a search in chat mode, creating a new chat.
 */
function handleChat() {
  if (!searchStore.chatSearchMode) return;

  chatStore.addChat();
  chatApiStore.handleSendChatMessage(chatStore.currentChat, currentText.value);
  layoutStore.mode = "chat";
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
      selectionStore.selectArtifact(artifacts[0].id);
    } else {
      selectionStore.clearSelections();
    }
  }
);

watch(
  () => artifactStore.selectedArtifact,
  (artifact) => {
    if (
      !searchStore.basicSearchMode ||
      !artifact ||
      searchStore.searchItems?.[0] === artifact
    )
      return;

    searchStore.searchItems = [artifact];
  }
);
</script>

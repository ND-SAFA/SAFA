<template>
  <q-select
    v-model="value"
    dense
    outlined
    use-input
    clearable
    dark
    :options-dark="false"
    label="Search Artifacts"
    style="min-width: 200px; width: 30vw"
    color="accent"
    class="q-ma-sm nav-input"
    data-cy="input-artifact-search-nav"
    :options="options"
    option-label="name"
    option-value="id"
    @filter="filterOptions"
  >
    <template #prepend>
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
      <artifact-body-display
        v-bind="itemProps"
        clickable
        display-title
        :artifact="opt"
        data-cy="text-artifact-search-item"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * Artifact search bar.
 */
export default {
  name: "ProjectSearchbar",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ArtifactSchema } from "@/types";
import { filterArtifacts } from "@/util";
import { artifactStore, selectionStore } from "@/hooks";
import {
  ArtifactBodyDisplay,
  Typography,
  FlexBox,
  Icon,
} from "@/components/common";

const options = ref(artifactStore.currentArtifacts);

/**
 * Returns the display text for how many matches there are.
 */
const matchText = computed(() => {
  const count = options.value.length;

  return count === 1 ? "1 Match" : `${count} Matches`;
});

const value = computed({
  get() {
    return selectionStore.selectedArtifact;
  },
  set(artifact: ArtifactSchema | undefined) {
    if (artifact) {
      selectionStore.viewArtifactSubtree(artifact.id);
    } else {
      selectionStore.clearSelections();
    }
  },
});

function filterOptions(search: string, update: (fn: () => void) => void) {
  if (search === "") {
    update(() => (options.value = artifactStore.currentArtifacts));
  } else {
    update(() => {
      options.value = artifactStore.currentArtifacts.filter((artifact) =>
        filterArtifacts(artifact, search)
      );
    });
  }
}

watch(
  () => artifactStore.currentArtifacts,
  (artifacts) => (options.value = artifacts)
);
</script>

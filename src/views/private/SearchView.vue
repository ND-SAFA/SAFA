<template>
  <private-page full-window>
    <flex-box full-width justify="center" t="10">
      <q-card>
        <flex-box>
          <q-select
            v-model="mode"
            outlined
            label="Search Mode"
            :options="modes"
            option-label="id"
            option-value="id"
            emit-value
            class="nav-search-mode"
            style="min-width: 150px"
          >
            <template #option="{ opt, itemProps }">
              <q-separator v-if="opt.id === 'Search'" />
              <list-item
                clickable
                :title="opt.id"
                :subtitle="opt.name"
                v-bind="itemProps"
              />
            </template>
          </q-select>
          <q-select
            ref="searchEl"
            v-model="searchItems"
            outlined
            use-input
            clearable
            multiple
            :label="placeholder"
            :options="options"
            :option-label="artifactLikeMode ? 'name' : undefined"
            :option-value="artifactLikeMode ? 'id' : undefined"
            input-debounce="0"
            class="nav-search-prompt"
            style="min-width: 600px"
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
              <artifact-body-display
                v-if="artifactLikeMode"
                v-bind="itemProps"
                clickable
                display-title
                :artifact="opt"
                data-cy="text-artifact-search-item"
              />
              <list-item v-else v-bind="itemProps" clickable :title="opt" />
            </template>
            <template v-if="mode !== 'Search'" #no-option>
              <flex-box column y="2" x="2">
                <flex-box full-width>
                  <artifact-type-input
                    v-model="searchTypes"
                    multiple
                    clearable
                    label="Search Artifact Types"
                    hint="What types am I generating relationships to."
                    class="full-width"
                    style="min-width: 250px"
                  />
                  <text-input
                    v-model="maxResults"
                    type="number"
                    label="Max Results"
                    class="q-ml-sm"
                    style="min-width: 125px; width: 125px"
                  />
                </flex-box>
                <artifact-type-input
                  v-model="relateTypes"
                  multiple
                  clearable
                  label="Include Artifact Types"
                  hint="What types do I want to see related to my search."
                  class="full-width q-my-md"
                  style="min-width: 250px"
                />
                <flex-box full-width justify="end">
                  <q-btn color="primary"> Search </q-btn>
                </flex-box>
              </flex-box>
            </template>
          </q-select>
        </flex-box>
      </q-card>
    </flex-box>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the project search page.
 */
export default {
  name: "SearchView",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ArtifactSchema, SelectOption } from "@/types";
import { filterArtifacts } from "@/util";
import { artifactStore, typeOptionsStore } from "@/hooks";
import {
  PrivatePage,
  FlexBox,
  Icon,
  ArtifactTypeInput,
  ListItem,
  TextInput,
  ArtifactBodyDisplay,
  Typography,
} from "@/components";

type Mode = "Prompt" | "Artifact" | "Artifact Type" | "Search";

const modes: SelectOption[] = [
  { id: "Prompt", name: "Find artifacts that match a search prompt." },
  { id: "Artifact", name: "Find artifacts related to a specific artifact." },
  {
    id: "Artifact Type",
    name: "Find artifacts related to a specific artifact type.",
  },
  {
    id: "Search",
    name: "Search through currently displayed artifacts.",
  },
];

const mode = ref<Mode>("Prompt");
const searchItems = ref<string[]>([]);
const searchTypes = ref<string[]>([]);
const maxResults = ref<number>(5);
const relateTypes = ref<string[]>([]);
const options = ref<ArtifactSchema[] | string[]>([]);

const artifactLikeMode = computed(() =>
  ["Artifact", "Search"].includes(mode.value)
);

const placeholder = computed(
  () =>
    ({
      Prompt: "Enter a prompt...",
      Artifact: "Search artifacts...",
      "Artifact Type": "Search artifact types...",
      Search: "Search current artifacts...",
    }[mode.value])
);

/**
 * Returns the display text for how many matches there are.
 */
const matchText = computed(() => {
  const count = options.value.length;

  return count === 1 ? "1 Match" : `${count} Matches`;
});

/**
 * Clears options if an item has been selected.
 */
function clearOptions(): void {
  options.value = searchItems.value.length > 0 ? [] : options.value;
}

/**
 * Filters the options based on the search text.
 * @param search - The search text.
 * @param update - A function called to update the options.
 */
function filterOptions(search: string, update: (fn: () => void) => void) {
  if (search === "" || searchItems.value.length > 0) {
    update(() => (options.value = []));
  } else {
    update(() => {
      if (artifactLikeMode.value) {
        options.value = artifactStore.currentArtifacts.filter((artifact) =>
          filterArtifacts(artifact, search)
        );
      } else if (mode.value === "Artifact Type") {
        const lowercaseSearch = search.toLowerCase();

        options.value = typeOptionsStore.artifactTypes.filter((type) =>
          type.toLowerCase().includes(lowercaseSearch)
        );
      } else {
        options.value = [];
      }
    });
  }
}

watch(
  () => mode.value,
  () => {
    searchItems.value = [];
  }
);
</script>

<style lang="scss">
.nav-search-mode {
  & > .q-field__inner > .q-field__control {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;

    &:before {
      border-right: none;
    }
  }
}

.nav-search-prompt {
  & > .q-field__inner > .q-field__control {
    border-bottom-left-radius: 0;
    border-top-left-radius: 0;
  }
}
</style>

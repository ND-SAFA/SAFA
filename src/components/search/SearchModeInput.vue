<template>
  <q-select
    v-model="searchStore.mode"
    outlined
    label="Search Mode"
    :options="modeOptions"
    option-label="name"
    option-value="id"
    class="nav-input nav-search-mode nav-multi-input-left"
    data-cy="input-nav-search-mode"
  >
    <template #option="{ opt, itemProps }">
      <separator v-if="opt.id === SearchMode.search" />
      <list-item
        clickable
        :title="opt.name"
        :subtitle="opt.description"
        v-bind="itemProps"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * Displays an input for selecting the type of search to perform.
 */
export default {
  name: "SearchModeInput",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { SearchMode } from "@/types";
import { searchModeOptions } from "@/util";
import { permissionStore, searchStore } from "@/hooks";
import { ListItem, Separator } from "@/components/common";

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const modeOptions = computed(() =>
  displayActions.value ? searchModeOptions() : [searchModeOptions()[2]]
);

/**
 * Clear the search data when the mode changes.
 */
watch(
  () => searchStore.mode,
  () => searchStore.clearSearch()
);
</script>

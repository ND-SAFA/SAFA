<template>
  <artifact-body-display
    v-if="artifactLikeMode"
    clickable
    display-title
    :artifact="props.option as ArtifactSchema"
    data-cy="text-artifact-search-item"
  />
  <list-item v-else clickable :title="props.option as string" />
</template>

<script lang="ts">
/**
 * Displays a selectable artifact or artifact type option in the searchbar.
 */
export default {
  name: "SearchOption",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactSchema, SearchOptionProps } from "@/types";
import { searchStore } from "@/hooks";
import { ListItem } from "@/components/common";
import { ArtifactBodyDisplay } from "@/components/artifact/display";

const props = defineProps<SearchOptionProps>();

const artifactLikeMode = computed(() => searchStore.artifactLikeMode);
</script>

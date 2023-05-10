<template>
  <artifact-body-display
    v-if="artifactLikeMode"
    clickable
    display-title
    :artifact="props.option"
    data-cy="text-artifact-search-item"
  />
  <list-item v-else clickable :title="props.option" />
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
import { ArtifactSchema } from "@/types";
import { searchStore } from "@/hooks";
import { ListItem, ArtifactBodyDisplay } from "@/components/common";

const props = defineProps<{
  /**
   * The option to display, either an artifact or artifact type.
   */
  option: ArtifactSchema | string;
}>();

const artifactLikeMode = computed(() => searchStore.artifactLikeMode);
</script>

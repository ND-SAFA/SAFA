<template>
  <flex-box column y="2" x="2">
    <flex-box full-width>
      <artifact-type-input
        v-model="searchStore.searchTypes"
        multiple
        clearable
        label="Search Artifact Types"
        hint="What types am I generating relationships to."
        class="full-width"
        style="min-width: 250px"
      />
      <text-input
        v-model="searchStore.maxResults"
        type="number"
        label="Max Results"
        class="q-ml-sm"
        style="min-width: 125px; width: 125px"
      />
    </flex-box>
    <artifact-type-input
      v-model="searchStore.relatedTypes"
      multiple
      clearable
      label="Include Artifact Types"
      hint="What types do I want to see related to my search."
      class="full-width q-my-md"
      style="min-width: 250px"
    />
    <flex-box full-width justify="end">
      <text-button color="primary" label="Search" @click="emit('submit')" />
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays inputs for refining a search query and generating search results.
 */
export default {
  name: "SearchInputs",
};
</script>

<script setup lang="ts">
import { searchStore } from "@/hooks";
import {
  FlexBox,
  ArtifactTypeInput,
  TextInput,
  TextButton,
} from "@/components/common";

const emit = defineEmits<{
  (e: "submit"): void;
}>();
</script>

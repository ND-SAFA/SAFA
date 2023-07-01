<template>
  <flex-box column y="2" x="2" style="max-width: 40vw">
    <artifact-type-input
      v-model="searchStore.searchTypes"
      multiple
      clearable
      label="Search Artifact Types"
      hint="What types am I generating relationships to."
      class="full-width"
      style="min-width: 250px"
    />
    <flex-box
      full-width
      :column="advancedOpen"
      :align="advancedOpen ? 'end' : 'center'"
    >
      <expansion-item
        v-model="advancedOpen"
        label="Advanced Search"
        class="full-width q-my-sm"
        style="transition: width 0.5s ease-in-out"
      >
        <flex-box full-width>
          <artifact-type-input
            v-model="searchStore.relatedTypes"
            multiple
            clearable
            label="Include Artifact Types"
            hint="What types do I want to see related to my search."
            class="full-width"
          />
          <text-input
            v-model="searchStore.maxResults"
            type="number"
            label="Max Results"
            class="q-ml-sm"
            hint="The maximum number of search results to display."
            style="min-width: 130px"
          />
        </flex-box>
      </expansion-item>
      <text-button
        v-close-popup
        align="end"
        color="primary"
        label="Search"
        class="q-ml-sm"
        @click="emit('submit')"
      />
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
import { ref } from "vue";
import { searchStore } from "@/hooks";
import {
  FlexBox,
  ArtifactTypeInput,
  TextInput,
  TextButton,
  ExpansionItem,
} from "@/components/common";

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const advancedOpen = ref(false);
</script>

<template>
  <flex-box
    v-if="props.panel.variant === 'trace'"
    full-width
    align="center"
    y="2"
  >
    <select-input
      v-model="props.panel.type"
      label="Source Type"
      :options="artifactTypes"
      hint="Required"
      class="full-width"
      data-cy="input-source-type"
    />
    <icon class="q-mx-sm" variant="trace" size="sm" />
    <select-input
      v-model="props.panel.toType"
      label="Target Type"
      :options="artifactTypes"
      hint="Required"
      class="full-width"
      data-cy="input-target-type"
    />
  </flex-box>
  <text-input
    v-if="props.panel.variant === 'artifact'"
    v-model="props.panel.type"
    label="Artifact Type"
    hint="Required"
    data-cy="input-artifact-type"
  />
</template>

<script lang="ts">
/**
 * Provides inputs for the file panel name.
 */
export default {
  name: "UploadPanelName",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { FilePanelProps } from "@/types";
import { projectSaveStore } from "@/hooks";
import { FlexBox, TextInput, Icon, SelectInput } from "@/components/common";

const props = defineProps<FilePanelProps>();

const artifactTypes = computed(() => projectSaveStore.artifactTypes);
</script>

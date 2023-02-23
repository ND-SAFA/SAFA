<template>
  <file-list-step
    label="Artifact Type"
    :panels="panels"
    @panel:add="handleAddPanel"
    @panel:delete="handleDeletePanel"
  >
    <template #panel="{ panel }">
      <text-input v-model="panel.name" label="Artifact Type" />
    </template>
  </file-list-step>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading sets of artifacts.
 */
export default {
  name: "ArtifactTypeStep",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { TextInput } from "@/components/common";
import FileListStep from "./FileListStep.vue";

// const props = defineProps<{}>();

// const emit = defineEmits<{}>();

const createEmptyPanel = () => ({
  name: "",
  open: true,
  ignoreErrors: false,
  file: undefined as File | undefined,
});

const panels = ref([createEmptyPanel()]);

/**
 * Adds a new panel.
 */
function handleAddPanel(): void {
  panels.value.push(createEmptyPanel());
}

/**
 * Deletes a panel.
 * @param index - The panel index to delete.
 */
function handleDeletePanel(index: number): void {
  panels.value = panels.value.filter((_, i) => i !== index);
}
</script>

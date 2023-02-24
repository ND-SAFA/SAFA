<template>
  <file-panel-list
    label="Artifact Type"
    :panels="panels"
    @panel:add="handleAddPanel"
    @panel:delete="handleDeletePanel"
  >
    <template #panel="{ panel }">
      <text-input v-model="panel.type" label="Artifact Type" hint="Required" />
    </template>
  </file-panel-list>
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
import { CreatorFilePanel } from "@/types";
import { TextInput } from "@/components/common";
import FilePanelList from "./FilePanelList.vue";

// const props = defineProps<{}>();

// const emit = defineEmits<{}>();

const createEmptyPanel = (): CreatorFilePanel => ({
  variant: "artifact",
  name: "",
  type: "",
  open: true,
  ignoreErrors: false,
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

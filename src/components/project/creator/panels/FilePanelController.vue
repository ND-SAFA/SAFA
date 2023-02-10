<template>
  <file-panel
    v-model:ignore-errors="ignoreErrors"
    :show-file-uploader="!isGeneratedToggle"
    :errors="panel.projectFile.errors"
    :entity-names="panel.entityNames"
    :entities-are-fab="!isTracePanel(panel)"
    :is-loading="isLoading"
    @change="handleChange"
    @delete="emit('delete')"
    @validate="handleValidate"
  >
    <template #title>
      <typography el="h2" variant="subtitle" :value="panel.title" />
    </template>

    <template v-if="isTracePanel(panel)" #before-rows>
      <switch-input v-model="isGeneratedToggle" label="Generate Trace Links" />
      <gen-method-input v-if="isGeneratedToggle" v-model="method" />
    </template>
  </file-panel>
</template>

<script lang="ts">
/**
 * Controls a file panel.
 */
export default {
  name: "FilePanelController",
};
</script>

<script setup lang="ts">
import { computed, ref, watch, defineProps, defineEmits } from "vue";
import {
  ArtifactMap,
  ParseFilePanel,
  ModelType,
  ValidFileTypes,
} from "@/types";
import { isTracePanel } from "@/util";
import { SwitchInput, GenMethodInput, Typography } from "@/components/common";
import FilePanel from "./FilePanel.vue";

const props = defineProps<{
  artifactMap: ArtifactMap;
  panel: ParseFilePanel<ArtifactMap, ValidFileTypes>;
}>();

const emit = defineEmits<{
  (e: "validate", isValid: boolean): void;
  (e: "delete"): void;
}>();

const isLoading = ref(false);
const ignoreErrors = ref(false);
const isGeneratedToggle = ref(false);

const method = computed({
  get() {
    if (isTracePanel(props.panel)) {
      return props.panel.projectFile.method;
    } else {
      return ModelType.NLBert;
    }
  },
  set(newMethod): void {
    if (isTracePanel(props.panel)) {
      props.panel.projectFile.method = newMethod;
    }
  },
});

/**
 * Parses added files.
 * @param file - The file to parse.
 */
async function handleChange(file: File | undefined): Promise<void> {
  if (file === undefined) {
    props.panel.clearPanel();
  } else {
    isLoading.value = true;
    await props.panel.parseFile(props.artifactMap, file);
    isLoading.value = false;
  }
}

/**
 * Sets whether the panel is valid, and emits that change.
 * @param isValid - Whether the panel is valid.
 */
function handleValidate(isValid: boolean): void {
  props.panel.projectFile.isValid = isValid;
  emit("validate", isValid);
}

watch(
  () => isGeneratedToggle.value,
  (isGenerated) => {
    if (!isTracePanel(props.panel)) return;

    props.panel.projectFile.isGenerated = isGenerated;
    props.panel.clearPanel();
  }
);
</script>

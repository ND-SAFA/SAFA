<template>
  <div>
    <file-format-alert />

    <list bordered class="q-my-lg">
      <file-panel
        v-for="(panel, idx) in panels"
        :key="idx"
        :panel="panel"
        :index="idx"
        :label="label"
        :new-label="newLabel"
        :variant="props.variant"
      >
        <template #panel>
          <slot name="panel" :panel="panel" />
        </template>
      </file-panel>
    </list>

    <flex-box justify="center">
      <text-button
        text
        icon="add"
        :label="newLabel"
        data-cy="button-add-panel"
        @click="handleAddPanel"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading files.
 */
export default {
  name: "FilePanelList",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { projectSaveStore } from "@/hooks";
import {
  TextButton,
  FlexBox,
  FileFormatAlert,
  List,
} from "@/components/common";
import FilePanel from "./FilePanel.vue";

const props = defineProps<{
  variant: "artifact" | "trace";
}>();

const emit = defineEmits<{
  (e: "validate", isValid: boolean): void;
}>();

const label = computed(() =>
  props.variant === "artifact" ? "Artifact Type" : "Trace Matrix"
);
const newLabel = computed(() => `New ${label.value}`);

const panels = computed(() =>
  props.variant === "artifact"
    ? projectSaveStore.artifactPanels
    : projectSaveStore.tracePanels
);

const isValid = computed(() =>
  panels.value
    .map(({ isValid }) => isValid)
    .reduce((acc, cur) => acc && cur, true)
);

/**
 * Adds a new panel.
 */
function handleAddPanel(): void {
  projectSaveStore.addPanel(props.variant);
}

watch(
  () => isValid.value,
  (valid) => emit("validate", valid)
);
</script>

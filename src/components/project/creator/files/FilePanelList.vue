<template>
  <div>
    <list :bordered="panels.length > 0" class="q-my-lg">
      <file-panel
        v-for="(panel, idx) in panels"
        :key="idx"
        :panel="panel"
        :index="idx"
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
        label="New Upload"
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
import { TextButton, FlexBox, List } from "@/components/common";
import FilePanel from "./FilePanel.vue";

const emit = defineEmits<{
  (e: "validate", isValid: boolean): void;
}>();

const panels = computed(() => [
  ...projectSaveStore.artifactPanels,
  ...projectSaveStore.tracePanels,
]);

const valid = computed(() =>
  panels.value.map(({ valid }) => valid).reduce((acc, cur) => acc && cur, true)
);

/**
 * Adds a new panel.
 */
function handleAddPanel(): void {
  projectSaveStore.addPanel("artifact");
}

watch(
  () => valid.value,
  (valid) => emit("validate", valid)
);
</script>

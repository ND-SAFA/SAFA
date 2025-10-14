<template>
  <div>
    <list class="q-mb-lg">
      <upload-panel
        v-for="(panel, idx) in panels"
        :key="idx"
        :panel="panel"
        :index="idx"
      >
        <template #panel>
          <slot name="panel" :panel="panel" />
        </template>
      </upload-panel>
    </list>

    <flex-box justify="center">
      <text-button
        v-if="allowMultiple"
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
  name: "UploadPanelList",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { projectSaveStore } from "@/hooks";
import { TextButton, FlexBox, List } from "@/components/common";
import UploadPanel from "./UploadPanel.vue";

const panels = computed(() => projectSaveStore.uploadPanels);

// Only allow multiple uploads when uploading individual files.
const allowMultiple = computed(() =>
  panels.value.reduce(
    (acc, { variant }) =>
      acc && (variant === "artifact" || variant === "trace"),
    true
  )
);

/**
 * Adds a new panel.
 */
function handleAddPanel(): void {
  projectSaveStore.addPanel("artifact");
}
</script>

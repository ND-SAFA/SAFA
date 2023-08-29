<template>
  <flex-box v-if="display" wrap t="2" class="settings-buttons">
    <q-btn-group flat>
      <text-button
        text
        label="Download"
        icon="download"
        data-cy="button-settings-download"
        @click="handleDownload"
      />
      <q-btn-dropdown auto-close dense>
        <text-button text label="CSV" @click="handleDownload" />
        <text-button text label="JSON" @click="handleDownload('json')" />
      </q-btn-dropdown>
    </q-btn-group>
    <separator vertical />
    <text-button
      text
      label="Edit"
      icon="edit"
      data-cy="button-settings-edit"
      @click="handleEdit"
    />
    <separator vertical />
    <text-button
      text
      label="Delete"
      icon="delete"
      data-cy="button-settings-delete"
      @click="handleDelete"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays buttons for interacting with projects.
 */
export default {
  name: "ProjectButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  identifierSaveStore,
  permissionStore,
  projectApiStore,
  projectStore,
} from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";

const display = computed(() => permissionStore.projectAllows("editor"));

/**
 * Opens the edit modal.
 */
function handleEdit(): void {
  identifierSaveStore.selectIdentifier(projectStore.project, "edit");
}

/**
 * Opens the edit modal.
 */
function handleDelete(): void {
  identifierSaveStore.selectIdentifier(projectStore.project, "delete");
}

/**
 * Downloads project files
 */
function handleDownload(fileType: "csv" | "json" = "csv"): void {
  projectApiStore.handleDownload(fileType);
}
</script>

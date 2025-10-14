<template>
  <flex-box wrap t="2" class="settings-buttons">
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
    <separator v-if="displayEditing" vertical />
    <text-button
      v-if="displayEditing"
      text
      label="Edit"
      icon="edit"
      data-cy="button-settings-edit"
      @click="handleEdit"
    />
    <separator v-if="displayDeleting" vertical />
    <text-button
      v-if="displayDeleting"
      text
      label="Transfer"
      icon="forward"
      data-cy="button-settings-transfer"
      @click="handleTransfer"
    />
    <separator v-if="displayDeleting" vertical />
    <text-button
      v-if="displayDeleting"
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

const displayEditing = computed(() =>
  permissionStore.isAllowed("project.edit")
);
const displayDeleting = computed(() =>
  permissionStore.isAllowed("project.delete")
);

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
 * Opens the transfer modal.
 */
function handleTransfer(): void {
  identifierSaveStore.selectIdentifier(projectStore.project, "transfer");
}

/**
 * Downloads project files
 */
function handleDownload(fileType: "csv" | "json" = "csv"): void {
  projectApiStore.handleDownload(fileType);
}
</script>

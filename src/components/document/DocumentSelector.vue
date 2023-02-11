<template>
  <v-select
    ref="documentSelector"
    :items="documentStore.projectDocuments"
    :model-value="documentStore.currentDocument"
    label="View"
    variant="outlined"
    color="accent"
    density="compact"
    hide-details
    dark
    style="max-width: 200px"
    class="mx-1 nav-input"
    item-text="name"
    data-cy="button-document-select-open"
    @update:model-value="handleSetDocument"
  >
    <template #item="{ item }">
      <v-row dense align="center" :data-cy-name="item.name">
        <v-col data-cy="button-document-select-item">
          {{ item.name }}
        </v-col>
        <v-col class="flex-grow-0" @click.stop="handleEditOpen(item)">
          <icon-button
            v-if="canEdit(item.name)"
            icon-id="mdi-dots-horizontal"
            :tooltip="`Edit ${item.name}`"
            data-cy="button-document-select-edit"
          />
        </v-col>
      </v-row>
    </template>

    <template #append-item>
      <text-button
        v-if="canEdit()"
        text
        block
        variant="add"
        data-cy="button-document-select-create"
        @click="handleCreateOpen"
      >
        Add View
      </text-button>
    </template>
  </v-select>
</template>

<script lang="ts">
/**
 * A selector for switching between documents.
 */
export default {
  name: "DocumentSelector",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { DocumentSchema } from "@/types";
import {
  appStore,
  documentSaveStore,
  documentStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { IconButton, TextButton } from "@/components/common";

const documentSelector = ref<HTMLElement | null>(null);

/**
 * Switches to the given document name.
 * @param documentName - The document name to switch to.
 */
function handleSetDocument(documentName: string) {
  const document = documentStore.projectDocuments.find(
    ({ name }) => documentName === name
  );

  if (!document) return;

  handleSwitchDocuments(document);
}
/**
 * Returns whether a document can be edited.
 * @param name - The document name, or none to check for general editing ability.
 * @return Whether editing is allowed.
 */
function canEdit(name = ""): boolean {
  return name !== "Default" && sessionStore.isEditor(projectStore.project);
}

/**
 * Closes the selector menu and resets all data.
 */
function handleCloseMenu() {
  documentSelector.value?.blur();
}

/**
 * Opens the document creation panel.
 */
function handleCreateOpen() {
  documentSaveStore.baseDocument = undefined;
  handleCloseMenu();
  appStore.openDetailsPanel("document");
}

/**
 * Opens the document edit panel.
 */
function handleEditOpen(document: DocumentSchema) {
  documentSaveStore.baseDocument = document;
  handleCloseMenu();
  appStore.openDetailsPanel("document");
}
</script>

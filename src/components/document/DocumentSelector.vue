<template>
  <q-select
    ref="documentSelector"
    v-model="document"
    dense
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    :options="documentStore.projectDocuments"
    label="View"
    class="nav-input"
    option-label="name"
    option-value="documentId"
    color="accent"
    style="width: 200px"
    data-cy="button-document-select-open"
  >
    <template #option="{ opt, itemProps }">
      <list-item v-bind="itemProps" :title="opt.name" :action-cols="2">
        <template #actions>
          <icon-button
            v-if="canEdit(opt.name)"
            v-close-popup
            icon="more"
            :tooltip="`Edit ${opt.name}`"
            data-cy="button-document-select-edit"
            @click="handleEditOpen(opt)"
          />
        </template>
      </list-item>
    </template>
    <template #after-options>
      <text-button
        v-if="canEdit()"
        v-close-popup
        text
        block
        label="Add View"
        icon="add"
        data-cy="button-document-select-create"
        @click="handleCreateOpen"
      />
    </template>
  </q-select>
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
import { computed, ref } from "vue";
import { DocumentSchema } from "@/types";
import {
  appStore,
  documentSaveStore,
  documentStore,
  projectStore,
  sessionStore,
  useTheme,
} from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { IconButton, TextButton, ListItem } from "@/components/common";

const documentSelector = ref<HTMLElement | null>(null);

const { darkMode } = useTheme();

const document = computed({
  get() {
    return documentStore.currentDocument;
  },
  set(document) {
    handleSwitchDocuments(document);
  },
});

/**
 * Returns whether a document can be edited.
 * @param name - The document name, or none to check for general editing ability.
 * @return Whether editing is allowed.
 */
function canEdit(name = ""): boolean {
  return name !== "Default" && sessionStore.isEditor(projectStore.project);
}

/**
 * Opens the document creation panel.
 */
function handleCreateOpen(): void {
  documentSaveStore.baseDocument = undefined;
  appStore.openDetailsPanel("document");
}

/**
 * Opens the document edit panel.
 */
function handleEditOpen(document: DocumentSchema): void {
  documentSaveStore.baseDocument = document;
  appStore.openDetailsPanel("document");
}
</script>

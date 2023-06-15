<template>
  <q-select
    v-model="document"
    dense
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    :options="options"
    label="View"
    class="nav-input nav-document"
    option-label="name"
    option-value="name"
    color="accent"
    data-cy="button-document-select-open"
  >
    <template v-if="canSave()" #append>
      <icon-button
        small
        tooltip="Save View"
        icon="save"
        data-cy="button-document-select-save"
        @click="handleSave"
      />
    </template>
    <template #option="{ opt, itemProps }">
      <list-item
        v-bind="itemProps"
        :title="opt.name"
        :action-cols="2"
        :data-cy-name="opt.name"
      >
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="canSave(opt)"
              small
              :tooltip="`Save ${opt.name}`"
              icon="save"
              data-cy="button-document-select-save"
              @click="handleSave"
            />
            <icon-button
              v-if="canEdit(opt.name)"
              v-close-popup
              small
              icon="more"
              :tooltip="`Edit ${opt.name}`"
              data-cy="button-document-select-edit"
              @click="handleEditOpen(opt)"
            />
          </flex-box>
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
import { computed } from "vue";
import { DocumentSchema } from "@/types";
import {
  appStore,
  documentSaveStore,
  documentStore,
  projectStore,
  sessionStore,
  useTheme,
} from "@/hooks";
import { handleCreatePresetDocument, handleSwitchDocuments } from "@/api";
import { IconButton, TextButton, ListItem, FlexBox } from "@/components/common";

const { darkMode } = useTheme();

const options = computed(() => documentStore.projectDocuments);

const document = computed({
  get() {
    return documentStore.currentDocument;
  },
  set(document) {
    handleSwitchDocuments(document);
  },
});

/**
 * Returns whether a document can be saved.
 * @param doc - The document to check.
 * @return Whether saving is allowed.
 */
function canSave(doc = document.value): boolean {
  return doc.name !== "Default" && !doc.documentId;
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

/**
 * Saves a new document.
 */
function handleSave(): void {
  handleCreatePresetDocument(document.value, {});
}
</script>

<template>
  <q-select
    v-model="viewApiStore.currentDocument"
    standout
    bg-color="transparent"
    class="nav-breadcrumb nav-view"
    options-selected-class="primary"
    :options="options"
    :disable="disabled"
    :loading="viewApiStore.loading"
    label="View"
    option-label="name"
    option-value="name"
    data-cy="button-document-select-open"
  >
    <template #append>
      <flex-box @click.stop="">
        <view-history />
        <icon-button
          v-if="canSave()"
          small
          tooltip="Save View"
          icon="save"
          data-cy="button-document-select-save"
          @click="handleSave"
        />
      </flex-box>
    </template>
    <template
      #option="{
        opt,
        itemProps,
      }: {
        opt: ViewSchema;
        itemProps: Record<string, unknown>;
      }"
    >
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
              icon="edit"
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
 * A selector for switching between views.
 */
export default {
  name: "ViewSelector",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ViewSchema } from "@/types";
import { DEFAULT_VIEW_NAME } from "@/util";
import {
  appStore,
  deltaStore,
  viewApiStore,
  documentSaveStore,
  documentStore,
  permissionStore,
} from "@/hooks";
import { IconButton, TextButton, ListItem, FlexBox } from "@/components/common";
import ViewHistory from "./ViewHistory.vue";

const options = computed(() => documentStore.projectDocuments);

const disabled = computed(() => deltaStore.inDeltaView);

/**
 * Returns whether a document can be saved.
 * @param doc - The document to check.
 * @return Whether saving is allowed.
 */
function canSave(doc = viewApiStore.currentDocument): boolean {
  return (
    doc.name !== DEFAULT_VIEW_NAME &&
    !doc.documentId &&
    permissionStore.isAllowed("project.edit_data")
  );
}

/**
 * Returns whether a document can be edited.
 * @param name - The document name, or none to check for general editing ability.
 * @return Whether editing is allowed.
 */
function canEdit(name = ""): boolean {
  return (
    name !== DEFAULT_VIEW_NAME && permissionStore.isAllowed("project.edit_data")
  );
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
function handleEditOpen(document: ViewSchema): void {
  documentSaveStore.baseDocument = document;
  appStore.openDetailsPanel("document");
}

/**
 * Saves a new document.
 */
function handleSave(): void {
  viewApiStore.handleCreatePreset(viewApiStore.currentDocument);
}
</script>

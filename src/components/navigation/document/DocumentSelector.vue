<template>
  <flex-box align="center">
    <v-select
      ref="documentSelector"
      v-model="select"
      :items="items"
      label="View"
      outlined
      color="accent"
      dense
      hide-details
      dark
      style="max-width: 200px"
      class="mx-1"
      item-text="name"
      data-cy="button-document-select-open"
    >
      <template v-slot:item="{ item }">
        <v-row dense align="center" :data-cy-name="item.name">
          <v-col data-cy="button-document-select-item">
            {{ item.name }}
          </v-col>
          <v-col class="flex-grow-0" @click.stop="handleEditOpen(item)">
            <generic-icon-button
              v-if="canEdit(item.name)"
              icon-id="mdi-dots-horizontal"
              :tooltip="`Edit ${item.name}`"
              data-cy="button-document-select-edit"
            />
          </v-col>
        </v-row>
      </template>

      <template v-slot:append-item>
        <v-btn
          v-if="canEdit()"
          text
          block
          color="primary"
          data-cy="button-document-select-create"
          @click="handleCreateOpen"
        >
          <v-icon>mdi-plus</v-icon>
          Add View
        </v-btn>

        <document-modal :is-open="isOpen" @close="handleCloseMenu" />
      </template>
    </v-select>
    <generic-icon-button
      color="accent"
      :icon-id="toggleViewIcon"
      :tooltip="toggleViewTooltip"
      data-cy="button-view-toggle"
      @click="handleToggleTableView"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentModel } from "@/types";
import {
  documentSaveStore,
  documentStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { GenericIconButton, FlexBox } from "@/components/common";
import DocumentModal from "./DocumentModal.vue";

export default Vue.extend({
  name: "DocumentSelector",
  components: { FlexBox, DocumentModal, GenericIconButton },
  data: () => ({
    isOpen: false,
  }),
  computed: {
    /**
     * @return The current documents.
     */
    items() {
      return documentStore.projectDocuments;
    },
    /**
     * @return The toggle document view icon.
     */
    toggleViewIcon(): string {
      return documentStore.isTableDocument
        ? "mdi-file-tree"
        : "mdi-table-multiple";
    },
    /**
     * @return The toggle document view tooltip.
     */
    toggleViewTooltip(): string {
      return documentStore.isTableDocument
        ? "Switch to tree view"
        : "Switch to table view";
    },
    /**
     * Switches documents when a document is selected.
     */
    select: {
      get() {
        return documentStore.currentDocument;
      },
      set(documentName: string) {
        const document = this.items.find(({ name }) => documentName === name);

        if (document) {
          handleSwitchDocuments(document);
        }
      },
    },
  },
  methods: {
    /**
     * Returns whether a document can be edited.
     * @param name - The document name, or none to check for general editing ability.
     * @return Whether editing is allowed.
     */
    canEdit(name = ""): boolean {
      return name !== "Default" && sessionStore.isEditor(projectStore.project);
    },
    /**
     * Closes the selector menu and resets all data.
     */
    handleCloseMenu() {
      (this.$refs.documentSelector as HTMLElement).blur();
      this.isOpen = false;
    },
    /**
     * Opens the create document modal.
     */
    handleCreateOpen() {
      documentSaveStore.baseDocument = undefined;
      this.isOpen = true;
    },
    /**
     * Opens the edit document modal.
     */
    handleEditOpen(document: DocumentModel) {
      documentSaveStore.baseDocument = document;
      this.isOpen = true;
    },
    /**
     * Switches between document views.
     */
    handleToggleTableView() {
      documentStore.toggleTableView();
    },
  },
});
</script>

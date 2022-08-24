<template>
  <flex-box align="center">
    <v-select
      ref="documentSelector"
      v-model="select"
      :items="items"
      label="View"
      outlined
      color="secondary"
      dense
      hide-details
      dark
      style="max-width: 200px"
      class="mx-1"
      item-text="name"
    >
      <template v-slot:item="{ item }">
        <v-row dense align="center">
          <v-col>
            {{ item.name }}
          </v-col>
          <v-col class="flex-grow-0" @click.stop="handleEditOpen(item)">
            <generic-icon-button
              v-if="item.name !== 'Default'"
              icon-id="mdi-dots-horizontal"
              :tooltip="`Edit ${item.name}`"
            />
          </v-col>
        </v-row>
      </template>

      <template v-slot:append-item>
        <v-btn text block color="primary" @click="handleCreateOpen">
          <v-icon>mdi-plus</v-icon>
          Add View
        </v-btn>

        <document-modal :is-open="isCreateOpen" @close="handleCloseMenu" />

        <document-modal
          :is-open="isEditOpen"
          :document="editingDocument"
          @close="handleCloseMenu"
        />
      </template>
    </v-select>
    <generic-icon-button
      color="white"
      :icon-id="toggleViewIcon"
      :tooltip="toggleViewTooltip"
      @click="handleToggleTableView"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentModel } from "@/types";
import { documentStore } from "@/hooks";
import { GenericIconButton, FlexBox } from "@/components/common";
import { handleSwitchDocuments } from "@/api";
import DocumentModal from "./DocumentModal.vue";

export default Vue.extend({
  name: "DocumentSelector",
  components: { FlexBox, DocumentModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    editingDocument: undefined as DocumentModel | undefined,
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
     * Closes the selector menu and resets all data.
     */
    handleCloseMenu() {
      (this.$refs.documentSelector as HTMLElement).blur();
      this.isEditOpen = false;
      this.isCreateOpen = false;
      this.editingDocument = undefined;
    },
    /**
     * Opens the create document modal.
     */
    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    /**
     * Opens the edit document modal.
     */
    handleEditOpen(document: DocumentModel) {
      this.editingDocument = document;
      this.isEditOpen = true;
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

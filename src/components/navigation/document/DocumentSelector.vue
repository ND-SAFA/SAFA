<template>
  <div class="d-flex flex-row align-center">
    <v-select
      ref="documentSelector"
      v-model="select"
      :items="items"
      label="Document"
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
          Add Document
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
      color="secondary"
      :icon-id="toggleViewIcon"
      :tooltip="toggleViewTooltip"
      @click="handleToggleTableView"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectDocument } from "@/types";
import { documentModule } from "@/store";
import { GenericIconButton } from "@/components/common/generic";
import DocumentModal from "./DocumentModal.vue";

export default Vue.extend({
  name: "DocumentSelector",
  components: { DocumentModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    editingDocument: undefined as ProjectDocument | undefined,
  }),
  computed: {
    /**
     * @return The current documents.
     */
    items() {
      return documentModule.projectDocuments;
    },
    /**
     * @return The toggle document view icon.
     */
    toggleViewIcon(): string {
      return documentModule.isTableDocument
        ? "mdi-file-tree"
        : "mdi-table-multiple";
    },
    /**
     * @return The toggle document view tooltip.
     */
    toggleViewTooltip(): string {
      return documentModule.isTableDocument
        ? "Switch to tree view"
        : "Switch to table view";
    },
    /**
     * Switches documents when a document is selected.
     */
    select: {
      get() {
        return documentModule.document;
      },
      set(documentName: string) {
        const document = this.items.find(({ name }) => documentName === name);

        if (document) {
          documentModule.switchDocuments(document);
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
    handleEditOpen(document: ProjectDocument) {
      this.editingDocument = document;
      this.isEditOpen = true;
    },
    /**
     * Switches between document views.
     */
    handleToggleTableView() {
      documentModule.toggleTableView();
    },
  },
});
</script>

<template>
  <v-select
    v-model="select"
    :items="items"
    label="Document"
    outlined
    color="secondary"
    dense
    hide-details
    dark
    style="width: 200px"
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

      <generic-modal
        title="Add Document"
        size="sm"
        :is-open="isCreateOpen"
        @close="handleCreateClose"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="documentName"
            :error-messages="nameErrors"
          />
        </template>
        <template v-slot:actions>
          <v-spacer />
          <v-btn
            color="primary"
            :disabled="!isDocumentValid"
            @click="handleAddDocument"
          >
            Create Document
          </v-btn>
        </template>
      </generic-modal>

      <generic-modal
        title="Edit Document"
        size="sm"
        :is-open="isEditOpen"
        @close="handleEditClose"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="documentName"
            :error-messages="nameErrors"
          />
        </template>
        <template v-slot:actions>
          <v-spacer />
          <v-btn
            color="primary"
            :disabled="!isDocumentValid"
            @click="handleEditDocument"
          >
            Confirm
          </v-btn>
        </template>
      </generic-modal>
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectDocument } from "@/types";
import { addNewDocument, editDocument } from "@/api";
import { createDocument } from "@/util";
import { documentModule } from "@/store";
import { GenericIconButton } from "@/components/common";
import GenericModal from "@/components/common/generic/GenericModal.vue";

export default Vue.extend({
  name: "DocumentSelector",
  components: { GenericModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    documentName: "",
    editingDocument: undefined as ProjectDocument | undefined,
  }),
  computed: {
    items(): ProjectDocument[] {
      return documentModule.projectDocuments;
    },
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

    isNameValid(): boolean {
      return (
        !documentModule.doesDocumentExist(this.documentName) ||
        this.editingDocument?.name === this.documentName
      );
    },
    isDocumentValid(): boolean {
      return !!this.documentName && this.isNameValid;
    },
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
  },
  methods: {
    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    handleCreateClose() {
      this.isCreateOpen = false;
    },
    handleAddDocument() {
      addNewDocument(createDocument([], this.documentName));
      this.handleCreateClose();
    },

    handleEditOpen(document: ProjectDocument) {
      this.isEditOpen = true;
      this.documentName = document.name;
      this.editingDocument = document;
    },
    handleEditClose() {
      this.isEditOpen = false;
      this.documentName = "";
      this.editingDocument = undefined;
    },
    handleEditDocument() {
      if (this.editingDocument) {
        this.editingDocument.name = this.documentName;
        editDocument(this.editingDocument);
      }

      this.handleEditClose();
    },
  },
});
</script>

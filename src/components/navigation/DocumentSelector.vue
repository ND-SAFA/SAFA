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
        @close="resetModalData"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="documentName"
            :error-messages="nameErrors"
          />
          <artifact-input v-model="artifactIds" />
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
        @close="resetModalData"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="documentName"
            :error-messages="nameErrors"
          />
          <artifact-input v-model="artifactIds" />
        </template>
        <template v-slot:actions>
          <v-btn
            color="error"
            :text="!confirmDelete"
            :outlined="confirmDelete"
            @click="handleDeleteDocument"
          >
            {{ confirmDelete ? "Delete" : "Delete Document" }}
          </v-btn>
          <v-btn outlined v-if="confirmDelete" @click="confirmDelete = false">
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            :disabled="!isDocumentValid"
            @click="handleEditDocument"
          >
            Confirm Edit
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
import {
  artifactModule,
  documentModule,
  logModule,
  projectModule,
} from "@/store";
import { ArtifactInput, GenericIconButton, GenericModal } from "@/components";
import { deleteDocument } from "@/api/endpoints/document-api";

export default Vue.extend({
  name: "DocumentSelector",
  components: { GenericModal, GenericIconButton, ArtifactInput },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    documentName: "",
    artifactIds: [] as string[],
    editingDocument: undefined as ProjectDocument | undefined,
    confirmDelete: false,
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
    resetModalData() {
      this.documentName = "";
      this.artifactIds = [];
      this.editingDocument = undefined;
      this.isCreateOpen = false;
      this.isEditOpen = false;
      this.confirmDelete = false;
    },

    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    handleAddDocument() {
      addNewDocument(
        createDocument(
          projectModule.getProject,
          this.artifactIds,
          this.documentName
        )
      );
      this.resetModalData();
    },

    handleEditOpen(document: ProjectDocument) {
      console.log(document.artifactIds);
      this.documentName = document.name;
      this.editingDocument = document;
      this.artifactIds = artifactModule.allArtifacts
        .filter(({ id }) => document.artifactIds?.includes(id))
        .map(({ id }) => id);
      this.isEditOpen = true;
    },
    handleEditDocument() {
      if (this.editingDocument) {
        this.editingDocument.name = this.documentName;
        this.editingDocument.artifactIds = this.artifactIds;
        editDocument(this.editingDocument);
      }

      this.resetModalData();
    },
    handleDeleteDocument() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else if (this.editingDocument) {
        deleteDocument(this.editingDocument)
          .then(async (document) => {
            logModule.onSuccess(
              `Successfully deleted document: ${document.name}`
            );
            await documentModule.removeDocument(document);
            this.resetModalData();
          })
          .catch(() => {
            logModule.onError(
              `Unable to delete document: ${this.documentName}`
            );
          });
      }
    },
  },
});
</script>

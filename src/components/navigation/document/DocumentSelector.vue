<template>
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

      <document-modal :is-open="isCreateOpen" @close="handleCloseMenu" />

      <document-modal
        :is-open="isEditOpen"
        :document="editingDocument"
        @close="handleCloseMenu"
      />
    </template>
  </v-select>
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
  },
  methods: {
    handleCloseMenu() {
      (this.$refs.documentSelector as HTMLElement).blur();
      this.isEditOpen = false;
      this.isCreateOpen = false;
      this.editingDocument = undefined;
    },
    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    handleEditOpen(document: ProjectDocument) {
      this.editingDocument = document;
      this.isEditOpen = true;
    },
  },
});
</script>

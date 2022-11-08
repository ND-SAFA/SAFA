<template>
  <div v-if="documents.length > 0" class="mt-4">
    <typography el="h2" variant="subtitle" value="Views" />
    <v-divider />

    <v-list>
      <template v-for="(doc, idx) in documents">
        <v-divider :key="doc.documentId + '-div'" v-if="idx !== 0" />
        <generic-list-item
          :key="doc.documentId"
          :item="{ title: doc.name, subtitle: documentTypeName(doc.type) }"
          @click="handleSwitchDocument(doc)"
        />
      </template>
    </v-list>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentModel } from "@/types";
import { documentTypeOptions } from "@/util";
import { documentStore, selectionStore } from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { Typography, GenericListItem } from "@/components/common";

/**
 * Displays the selected node's documents.
 */
export default Vue.extend({
  name: "ArtifactDocuments",
  components: { Typography, GenericListItem },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's documents.
     */
    documents(): DocumentModel[] {
      if (!this.selectedArtifact) return [];

      return documentStore.projectDocuments.filter(({ documentId }) =>
        this.selectedArtifact?.documentIds.includes(documentId)
      );
    },
  },
  methods: {
    /**
     * Switches to another document.
     * @param document - The document to switch to.
     */
    handleSwitchDocument(document: DocumentModel): void {
      handleSwitchDocuments(document);
    },
    /**
     * Converts the document type into a display name.
     * @param typeId - The document type id.
     * @return The document type name.
     */
    documentTypeName(typeId: string): string {
      return (
        documentTypeOptions().find(({ id }) => id === typeId)?.name || typeId
      );
    },
  },
});
</script>

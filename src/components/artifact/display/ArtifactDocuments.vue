<template>
  <panel-card v-if="doDisplay">
    <typography el="h2" variant="subtitle" value="Views" />
    <v-divider />

    <v-list>
      <template v-for="(doc, idx) in documents">
        <v-divider :key="doc.documentId + '-div'" v-if="idx !== 0" />
        <list-item
          :key="doc.documentId"
          :item="{ title: doc.name, subtitle: documentTypeName(doc.type) }"
          @click="handleSwitchDocument(doc)"
        />
      </template>
    </v-list>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentSchema } from "@/types";
import { documentTypeOptions } from "@/util";
import { documentStore, selectionStore } from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { Typography, ListItem, PanelCard } from "@/components/common";

/**
 * Displays the selected node's documents.
 */
export default Vue.extend({
  name: "ArtifactDocuments",
  components: { PanelCard, Typography, ListItem },
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
    documents(): DocumentSchema[] {
      if (!this.selectedArtifact) return [];

      return documentStore.projectDocuments.filter(({ documentId }) =>
        this.selectedArtifact?.documentIds.includes(documentId)
      );
    },
    /**
     * @return Whether to display this section.
     */
    doDisplay(): boolean {
      return this.documents.length > 0;
    },
  },
  methods: {
    /**
     * Switches to another document.
     * @param document - The document to switch to.
     */
    handleSwitchDocument(document: DocumentSchema): void {
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

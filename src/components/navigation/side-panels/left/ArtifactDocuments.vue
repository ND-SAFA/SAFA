<template>
  <div v-if="documents.length > 0" class="mt-4">
    <h2 class="text-h6">Documents</h2>
    <v-divider />

    <v-list>
      <v-list-item
        v-for="doc in documents"
        :key="doc.documentId"
        @click="handleSwitchDocument(doc)"
      >
        <v-list-item-title>
          {{ doc.name }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ documentTypeName(doc.type) }}
        </v-list-item-subtitle>
      </v-list-item>
    </v-list>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectDocument } from "@/types";
import { documentTypeOptions } from "@/util";
import { artifactSelectionModule, documentModule } from "@/store";

/**
 * Displays the selected node's documents.
 */
export default Vue.extend({
  name: "ArtifactDocuments",
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's documents.
     */
    documents(): ProjectDocument[] {
      if (!this.selectedArtifact) return [];

      return documentModule.projectDocuments.filter(({ documentId }) =>
        this.selectedArtifact?.documentIds.includes(documentId)
      );
    },
  },
  methods: {
    /**
     * Switches to another document.
     * @param document - The document to switch to.
     */
    handleSwitchDocument(document: ProjectDocument): void {
      documentModule.switchDocuments(document);
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

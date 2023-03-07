<template>
  <panel-card v-if="doDisplay" title="Views">
    <list>
      <list-item
        v-for="doc in documents"
        :key="doc.documentId"
        clickable
        tooltip
        :title="doc.name"
        :subtitle="documentTypeName(doc.type)"
        @click="handleSwitch(doc)"
      />
    </list>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's documents.
 */
export default {
  name: "ArtifactDocuments",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { DocumentSchema } from "@/types";
import { documentTypeOptions } from "@/util";
import { documentStore, selectionStore } from "@/hooks";
import { handleSwitchDocuments } from "@/api";
import { List, ListItem, PanelCard } from "@/components/common";

const artifact = computed(() => selectionStore.selectedArtifact);

const documents = computed(() =>
  artifact.value
    ? documentStore.projectDocuments.filter(({ documentId }) =>
        artifact.value?.documentIds.includes(documentId)
      )
    : []
);

const doDisplay = computed(() => documents.value.length > 0);

/**
 * Switches to another document.
 * @param document - The document to switch to.
 */
function handleSwitch(document: DocumentSchema): void {
  handleSwitchDocuments(document);
}

/**
 * Converts the document type into a display name.
 * @param typeId - The document type id.
 * @return The document type name.
 */
function documentTypeName(typeId: string): string {
  return documentTypeOptions().find(({ id }) => id === typeId)?.name || typeId;
}
</script>

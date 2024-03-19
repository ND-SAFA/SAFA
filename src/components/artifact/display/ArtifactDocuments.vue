<template>
  <panel-card v-if="doDisplay" title="Views" collapsable>
    <list>
      <list-item
        v-for="doc in documents"
        :key="doc.documentId"
        clickable
        tooltip
        :title="doc.name"
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
import { artifactStore, documentApiStore, documentStore } from "@/hooks";
import { List, ListItem, PanelCard } from "@/components/common";

const artifact = computed(() => artifactStore.selectedArtifact);

const documents = computed(() =>
  artifact.value
    ? documentStore.projectDocuments.filter(
        ({ documentId }) => artifact.value?.documentIds.includes(documentId)
      )
    : []
);

const doDisplay = computed(() => documents.value.length > 0);

/**
 * Switches to another document.
 * @param document - The document to switch to.
 */
function handleSwitch(document: DocumentSchema): void {
  documentApiStore.handleSwitch(document);
}
</script>

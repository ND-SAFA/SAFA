<template>
  <panel-card v-if="doDisplay" title="Views" collapsable borderless>
    <list>
      <list-item
        v-for="doc in documents"
        :key="doc.documentId"
        clickable
        tooltip
        :title="doc.name"
        @click="viewApiStore.handleSwitch(doc)"
      />
    </list>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's views.
 */
export default {
  name: "ArtifactViews",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore, viewApiStore, documentStore } from "@/hooks";
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
</script>

<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-fab />

      <artifact-creator-modal
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @close="closeArtifactCreator"
      />
      <trace-link-creator-modal
        :is-open="isTraceLinkCreatorOpen"
        @close="closeTraceLinkCreator"
      />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { artifactSelectionModule } from "@/store";
import { appStore } from "@/hooks";
import {
  ArtifactTree,
  ArtifactTable,
  PrivatePage,
  ArtifactCreatorModal,
  ArtifactFab,
  TraceLinkCreatorModal,
} from "@/components";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    TraceLinkCreatorModal,
    ArtifactFab,
    ArtifactTable,
    PrivatePage,
    ArtifactTree,
    ArtifactCreatorModal,
  },
  computed: {
    /**
     * Returns whether the artifact creator is open.
     */
    isArtifactCreatorOpen() {
      return appStore.isArtifactCreatorOpen;
    },
    /**
     * Returns whether the trace link creator is open.
     */
    isTraceLinkCreatorOpen() {
      return appStore.isTraceLinkCreatorOpen;
    },
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
  },
  methods: {
    /**
     * Closes the artifact creator.
     */
    closeArtifactCreator(): void {
      appStore.closeArtifactCreator();
    },
    /**
     * Closes the trace link creator.
     */
    closeTraceLinkCreator(): void {
      appStore.toggleTraceLinkCreator();
    },
  },
});
</script>

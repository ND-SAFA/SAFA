<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-tree-fab />

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
import { appModule, artifactSelectionModule } from "@/store";
import {
  ArtifactTree,
  ArtifactTable,
  PrivatePage,
  ArtifactCreatorModal,
  ArtifactTreeFab,
  TraceLinkCreatorModal,
} from "@/components";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    TraceLinkCreatorModal,
    ArtifactTreeFab,
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
      return appModule.getIsArtifactCreatorOpen;
    },
    /**
     * Returns whether the trace link creator is open.
     */
    isTraceLinkCreatorOpen() {
      return appModule.getIsTraceLinkCreatorOpen;
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
      appModule.closeArtifactCreator();
    },
    /**
     * Closes the trace link creator.
     */
    closeTraceLinkCreator(): void {
      appModule.toggleTraceLinkCreator();
    },
  },
});
</script>

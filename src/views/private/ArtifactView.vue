<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-creator-modal
        :title="creatorTitle"
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @close="closeArtifactCreator"
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
} from "@/components";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
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
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact.
     */
    creatorTitle() {
      return artifactSelectionModule.getSelectedArtifact
        ? "Edit Artifact"
        : "Create Artifact";
    },
  },
  methods: {
    /**
     * Closes the artifact creator.
     */
    closeArtifactCreator(): void {
      appModule.closeCreator();
    },
  },
});
</script>

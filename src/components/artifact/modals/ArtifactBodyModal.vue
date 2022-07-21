<template>
  <generic-modal
    :is-open="isOpen"
    :title="selectedArtifactName"
    :actionsHeight="0"
    size="l"
    @close="handleClose"
  >
    <template v-slot:body>
      <pre v-if="isCodeDisplay" class="text-body-1 mt-2 overflow-y-auto">
          {{ selectedArtifactBody }}
        </pre
      >
      <p class="text-body-1 mt-6">{{ selectedArtifactBody }}</p>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule, artifactSelectionModule } from "@/store";
import { GenericModal } from "@/components/common";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: {
    GenericModal,
  },
  computed: {
    isOpen() {
      return appModule.getIsArtifactBodyOpen;
    },
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    selectedArtifactName(): string {
      return this.selectedArtifact?.name || "";
    },
    /**
     * @return The selected artifact's body.
     */
    selectedArtifactBody(): string {
      return this.selectedArtifact?.body.trim() || "";
    },
    /**
     * An incredibly crude and temporary way to distinguish code nodes.
     *
     * @return Whether to display this body as code.
     */
    isCodeDisplay(): boolean {
      return this.selectedArtifact?.type.includes("code") || false;
    },
  },
  methods: {
    handleClose() {
      appModule.SET_ARTIFACT_BODY(false);
    },
  },
});
</script>

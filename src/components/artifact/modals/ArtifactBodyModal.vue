<template>
  <generic-modal
    :is-open="isOpen"
    :title="selectedArtifactName"
    :actionsHeight="0"
    size="l"
    @close="handleClose"
  >
    <template v-slot:body>
      <typography
        :variant="isCodeDisplay ? 'code' : 'body'"
        el="p"
        y="6"
        :value="selectedArtifactBody"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore, selectionStore } from "@/hooks";
import { GenericModal, Typography } from "@/components/common";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: {
    Typography,
    GenericModal,
  },
  computed: {
    isOpen() {
      return appStore.isArtifactBodyOpen;
    },
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
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
      appStore.toggleArtifactBody();
    },
  },
});
</script>

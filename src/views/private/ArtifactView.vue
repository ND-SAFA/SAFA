<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-creator-modal
        :is-open="isArtifactCreatorOpen"
        @close="closeArtifactCreator"
      />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule } from "@/store";
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

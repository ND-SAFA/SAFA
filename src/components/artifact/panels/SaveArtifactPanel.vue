<template>
  <div v-if="isOpen" data-cy="panel-artifact-save">
    <save-artifact />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { SaveArtifact } from "../save";

/**
 * Allows for creating and editing artifacts.
 */
export default Vue.extend({
  name: "SaveArtifactPanel",
  components: { SaveArtifact },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "saveArtifact";
    },
  },
});
</script>

<style scoped lang="scss"></style>

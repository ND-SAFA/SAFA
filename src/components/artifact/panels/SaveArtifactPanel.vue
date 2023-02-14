<template>
  <div v-if="isOpen" data-cy="panel-artifact-save">
    <save-artifact />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { appStore } from "@/hooks";
import { SaveArtifact } from "../save";

/**
 * Allows for creating and editing artifacts.
 */
export default defineComponent({
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

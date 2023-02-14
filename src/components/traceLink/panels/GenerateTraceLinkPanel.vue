<template>
  <div v-if="isOpen" data-cy="panel-trace-display">
    <trace-link-generator :is-open="isOpen" @submit="handleClose" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { appStore } from "@/hooks";
import { TraceLinkGenerator } from "../save";

/**
 * Displays trace link information.
 */
export default defineComponent({
  name: "TraceLinkPanel",
  components: { TraceLinkGenerator },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "generateTrace";
    },
  },
  methods: {
    /**
     * Closes all side panels.
     */
    handleClose(): void {
      appStore.closeSidePanels();
    },
  },
});
</script>

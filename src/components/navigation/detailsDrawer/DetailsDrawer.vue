<template>
  <v-navigation-drawer
    app
    right
    clipped
    hide-overlay
    :value="drawerOpen"
    height="100%"
  >
    <v-container>
      <generic-icon-button
        icon-id="mdi-close"
        tooltip="Close panel"
        @click="toggleOpen"
      />
      <span v-if="openState === 'delta'"> delta </span>
      <span v-if="openState === 'document'"> document </span>
      <span v-if="openState === 'displayArtifact'"> display artifact </span>
      <span v-if="openState === 'displayArtifactBody'">
        display artifact body
      </span>
      <span v-if="openState === 'saveArtifact'"> edit artifact </span>
      <span v-if="openState === 'displayTrace'"> display trace </span>
      <span v-if="openState === 'saveTrace'"> edit trace </span>
    </v-container>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { DetailsOpenState } from "@/types";
import { appStore } from "@/hooks";
import { GenericIconButton } from "@/components/common";

/**
 * Renders content in a right side panel.
 */
export default Vue.extend({
  name: "DetailsDrawer",
  components: { GenericIconButton },
  computed: {
    /**
     * @return The state of the details panel.
     */
    openState(): DetailsOpenState {
      return appStore.isDetailsPanelOpen;
    },
    /**
     * @return Whether the details panel is open.
     */
    drawerOpen(): boolean {
      return !!this.openState;
    },
  },
  methods: {
    /**
     * Toggles whether the details panel is open.
     */
    toggleOpen(): void {
      appStore.toggleDetailsPanel();
    },
  },
});
</script>

<style scoped lang="scss"></style>

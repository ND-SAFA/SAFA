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
    </v-container>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
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
     * @return Whether the details panel is open.
     */
    drawerOpen(): boolean {
      return appStore.isDetailsPanelOpen;
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

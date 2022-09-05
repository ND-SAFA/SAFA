<template>
  <v-navigation-drawer
    app
    clipped
    hide-overlay
    right
    stateless
    :value="isRightOpen"
    width="325"
    height="100%"
  >
    <project-details-panel />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import ProjectDetailsPanel from "./ProjectDetailsPanel.vue";

/**
 * Displays the right nav drawer.
 */
export default Vue.extend({
  name: "RightNavDrawer",
  components: {
    ProjectDetailsPanel,
  },
  computed: {
    /**
     * @return Whether the right panel is open.
     */
    isRightOpen: () => appStore.isRightPanelOpen,
  },
});
</script>

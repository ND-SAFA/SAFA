<template>
  <v-navigation-drawer
    app
    clipped
    hide-overlay
    light
    left
    stateless
    :value="isLeftOpen"
    width="250"
    height="100%"
  >
    <selected-node-tab />
  </v-navigation-drawer>
</template>
<script lang="ts">
import Vue from "vue";
import { appModule } from "@/store";
import SelectedNodeTab from "./SelectedNodeTab.vue";

/**
 * Displays the left nav drawer.
 */
export default Vue.extend({
  name: "LeftNavDrawer",
  components: {
    SelectedNodeTab,
  },
  computed: {
    /**
     * @return Whether the left panel is open.
     */
    isLeftOpen: () => appModule.getIsLeftOpen,
  },
});
</script>

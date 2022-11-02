<template>
  <v-app-bar app color="primary">
    <div class="full-width">
      <flex-box full-width justify="space-between">
        <flex-box align="center">
          <generic-icon-button
            v-if="sidebarOpen"
            icon-id="mdi-chevron-left"
            tooltip="Close sidebar"
            @click="sidebarOpen = false"
            color="accent"
          />
          <app-version />
        </flex-box>
        <flex-box align="center">
          <update-button />
          <saving-icon />
          <notifications />
        </flex-box>
      </flex-box>

      <v-divider class="accent faded mt-1" v-if="graphVisible" />
      <loading-bar />
    </div>
    <template v-slot:extension v-if="graphVisible">
      <graph-bar />
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { Route } from "vue-router";
import { appStore } from "@/hooks";
import { router, Routes } from "@/router";
import { GenericIconButton, FlexBox } from "@/components/common";
import GraphBar from "./GraphBar.vue";
import Notifications from "./Notifications.vue";
import AppVersion from "./AppVersion.vue";
import LoadingBar from "./LoadingBar.vue";
import SavingIcon from "./SavingIcon.vue";
import UpdateButton from "./UpdateButton.vue";

/**
 * Renders the top navigation bar.
 */
export default Vue.extend({
  name: "AppNavBar",
  components: {
    GraphBar,
    Notifications,
    SavingIcon,
    UpdateButton,
    AppVersion,
    FlexBox,
    GenericIconButton,
    LoadingBar,
  },
  data() {
    return {
      graphVisible: router.currentRoute.path === Routes.ARTIFACT,
    };
  },
  watch: {
    /**
     * Checks whether the graph buttons should be visible when the route changes.
     */
    $route(to: Route) {
      this.graphVisible = to.path === Routes.ARTIFACT;
    },
  },
  computed: {
    /**
     * Manages changes to the panel open state.
     */
    sidebarOpen: {
      get(): boolean {
        return appStore.isAppPanelOpen;
      },
      set() {
        appStore.toggleAppPanel();
      },
    },
  },
});
</script>

<style scoped lang="scss"></style>

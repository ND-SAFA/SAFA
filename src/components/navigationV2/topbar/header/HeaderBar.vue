<template>
  <div class="full-width">
    <flex-box full-width justify="space-between">
      <flex-box align="center">
        <searchbar v-if="graphVisible" />
        <notifications />
      </flex-box>
      <flex-box align="center">
        <update-button />
        <saving-icon />
        <app-version />
      </flex-box>
    </flex-box>
    <v-divider class="accent faded mt-2" v-if="graphVisible" />
    <loading-bar />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Route } from "vue-router";
import { router, Routes } from "@/router";
import { FlexBox } from "@/components/common";
import Searchbar from "./Searchbar.vue";
import Notifications from "./Notifications.vue";
import AppVersion from "./AppVersion.vue";
import SavingIcon from "./SavingIcon.vue";
import UpdateButton from "./UpdateButton.vue";
import LoadingBar from "./LoadingBar.vue";

/**
 * Renders the top navigation bar header.
 */
export default Vue.extend({
  name: "HeaderBar",
  components: {
    Searchbar,
    Notifications,
    SavingIcon,
    UpdateButton,
    AppVersion,
    FlexBox,
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
  computed: {},
});
</script>

<style scoped lang="scss"></style>

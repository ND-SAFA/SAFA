<template>
  <div style="position: absolute; bottom: 0" class="full-width">
    <v-list-item>
      <v-list-item-icon>
        <notifications />
      </v-list-item-icon>
      <v-list-item-title>
        <typography value="Notifications" />
      </v-list-item-title>
    </v-list-item>

    <v-divider />

    <v-list-item :to="accountPath">
      <v-list-item-icon>
        <v-icon color="primary">mdi-account-circle</v-icon>
      </v-list-item-icon>
      <v-list-item-title data-cy="page-account">
        <typography bold value="My Account" />
      </v-list-item-title>
    </v-list-item>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { Routes } from "@/router";
import { Typography } from "@/components/common";
import Notifications from "./Notifications.vue";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "NavAccount",
  components: { Notifications, Typography },
  data() {
    return { accountPath: Routes.ACCOUNT };
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

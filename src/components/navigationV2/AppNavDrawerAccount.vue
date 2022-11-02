<template>
  <div style="position: absolute; bottom: 0" class="full-width">
    <v-container v-if="sidebarOpen">
      <flex-box full-width justify="center" column>
        <v-btn text rounded @click="handleFeedback">Send Feedback</v-btn>
        <v-btn text rounded @click="handleWalkthrough">Walkthrough</v-btn>
        <v-btn text rounded @click="handleChangelog">Recent Changes</v-btn>
      </flex-box>
    </v-container>
    <v-divider />
    <v-list-item @click="handleEditAccount">
      <v-list-item-icon>
        <v-icon color="primary">mdi-account-circle</v-icon>
      </v-list-item-icon>
      <v-list-item-title>
        <typography bold value="My Account" />
      </v-list-item-title>
    </v-list-item>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { handleLogout } from "@/api";
import { FlexBox, Typography } from "@/components/common";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "AppNavDrawerAccount",
  components: { Typography, FlexBox },
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
  methods: {
    /**
     * Routes the user to the feedback page.
     */
    handleFeedback(): void {
      window.open(
        "https://www.notion.so/nd-safa/b73d1a8bfe0345f8b4d72daa1ceaf934?v=6e5d2439907a428fa1db2671a5eaa0b6"
      );
    },
    /**
     * Routes the user to the walkthrough page.
     */
    handleWalkthrough(): void {
      window.open(
        "https://www.notion.so/nd-safa/8dc14ae706074b099928afe13df39448?v=5b5e744919f84178bac1c96f5a5a92ba"
      );
    },
    /**
     * Routes the user to the walkthrough page.
     */
    handleChangelog(): void {
      window.open(
        "https://www.notion.so/nd-safa/5155dc357f534eb49f8071a03ce3ae32?v=74f671825a1b4d048909843740c003f1"
      );
    },
    /**
     * Logs the user out.
     */
    handleLogout(): void {
      handleLogout();
    },
    /**
     * Navigates to the account editing page.
     */
    handleEditAccount(): void {
      navigateTo(Routes.ACCOUNT);
    },
  },
});
</script>

<style scoped lang="scss"></style>

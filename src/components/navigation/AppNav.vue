<template>
  <div>
    <app-nav-bar v-if="isLoggedIn" />
    <app-nav-drawer v-if="isLoggedIn" />
    <details-drawer v-if="isLoggedIn" />
    <snackbar />
    <app-confirm-modal :message="confirmationMessage" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { logStore, sessionStore } from "@/hooks";
import { AppConfirmModal, Snackbar } from "@/components/common";
import { AppNavDrawer } from "./sidebar";
import { AppNavBar } from "./topbar";
import { DetailsDrawer } from "./detailsDrawer";

/**
 * Renders all app navigation bars.
 */
export default Vue.extend({
  name: "AppNav",
  components: {
    DetailsDrawer,
    AppNavBar,
    AppNavDrawer,
    AppConfirmModal,
    Snackbar,
  },
  computed: {
    /**
     * @return The current confirmation message, if one exists.
     */
    confirmationMessage() {
      return logStore.confirmation;
    },
    /**
     * Returns whether a user is currently logged in.
     */
    isLoggedIn() {
      return sessionStore.doesSessionExist;
    },
  },
});
</script>

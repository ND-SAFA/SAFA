<template>
  <div>
    <snackbar :timeout="5000" />
    <app-confirm-modal :message="confirmationMessage" />

    <artifact-body-modal v-if="isLoggedIn" />
    <app-bar v-if="isLoggedIn" />
    <left-nav-drawer v-if="isLoggedIn" />
    <right-nav-drawer v-if="isLoggedIn" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { logModule, sessionModule } from "@/store";
import { AppConfirmModal, ArtifactBodyModal, Snackbar } from "@/components";
import AppBar from "./AppBar.vue";
import { LeftNavDrawer, RightNavDrawer } from "./side-panels";

/**
 * Renders the navigation bars and top level modals.
 */
export default Vue.extend({
  name: "Navigation",
  components: {
    Snackbar,
    AppConfirmModal,
    ArtifactBodyModal,
    AppBar,
    LeftNavDrawer,
    RightNavDrawer,
  },
  computed: {
    /**
     * @return The current confirmation message, if one exists.
     */
    confirmationMessage() {
      return logModule.getConfirmationMessage;
    },
    /**
     * Returns whether a user is currently logged in.
     */
    isLoggedIn() {
      return sessionModule.getDoesSessionExist;
    },
  },
});
</script>

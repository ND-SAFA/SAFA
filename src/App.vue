<template>
  <v-app>
    <v-main>
      <transition name="fade" mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </transition>
    </v-main>

    <snackbar :timeout="5000" />
    <app-confirm-modal :message="confirmationMessage" />

    <artifact-body-modal v-if="isLoggedIn" />
    <app-bar v-if="isLoggedIn" />
    <left-nav-drawer v-if="isLoggedIn" />
    <right-nav-drawer v-if="isLoggedIn" />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { logModule, sessionModule } from "@/store";
import { handleAuthentication } from "@/api";
import {
  AppConfirmModal,
  ArtifactBodyModal,
  Snackbar,
  AppBar,
  LeftNavDrawer,
  RightNavDrawer,
} from "@/components";

/**
 * Renders the SAFA app.
 */
export default Vue.extend({
  name: "App",
  components: {
    Snackbar,
    AppConfirmModal,
    ArtifactBodyModal,
    AppBar,
    LeftNavDrawer,
    RightNavDrawer,
  },
  async mounted() {
    await handleAuthentication();
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

<style lang="scss">
@import "./assets/main.scss";
</style>

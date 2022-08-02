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
    <artifact-body-modal />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { logModule } from "@/store";
import { handleAuthentication } from "@/api";
import { AppConfirmModal, ArtifactBodyModal, Snackbar } from "@/components";

/**
 * Renders the SAFA app.
 */
export default Vue.extend({
  name: "App",
  components: {
    Snackbar,
    AppConfirmModal,
    ArtifactBodyModal,
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
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";
</style>

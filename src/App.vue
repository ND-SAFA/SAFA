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
    <artifact-creator-modal
      :is-open="isArtifactCreatorOpen"
      @close="closeArtifactCreator"
    />
    <app-confirm-modal :message="confirmationMessage" />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appModule, logModule } from "@/store";
import { handleAuthentication } from "@/api";
import { AppConfirmModal, ArtifactCreatorModal, Snackbar } from "@/components";

export default Vue.extend({
  name: "app",
  components: {
    Snackbar,
    ArtifactCreatorModal,
    AppConfirmModal,
  },
  async mounted() {
    await handleAuthentication();
  },
  computed: {
    isArtifactCreatorOpen: () => appModule.getIsArtifactCreatorOpen,
    confirmationMessage: () => logModule.getConfirmationMessage,
  },
  methods: {
    closeArtifactCreator(): void {
      appModule.closePanel(PanelType.artifactCreator);
    },
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";
</style>

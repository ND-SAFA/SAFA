<template>
  <v-app class="application">
    <v-main>
      <v-container class="elevation-4">
        <transition name="fade" mode="out-in">
          <keep-alive>
            <router-view />
          </keep-alive>
        </transition>
      </v-container>
    </v-main>
    <AppBar :isLeftOpen="isLeftOpen" :isRightOpen="isRightOpen" />
    <Snackbar :timeout="5000" />
    <LeftNavDrawer :isLeftOpen="isLeftOpen" :width="250" />
    <RightNavDrawer :isRightOpen="isRightOpen" :width="325" />
    <ArtifactCreator
      :isOpen="isArtifactCreatorOpen"
      @onClose="closeArtifactCreator"
    />
    <GenericConfirmDialog :message="confirmationMessage" />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Snackbar from "@/components/navigation/Snackbar.vue";
import LeftNavDrawer from "@/components/side-panels/left/LeftNavDrawer.vue";
import RightNavDrawer from "@/components/side-panels/right/RightNavDrawer.vue";
import AppBar from "@/components/navigation/AppBar.vue";
import ArtifactCreator from "@/components/common/modals/ArtifactCreatorModal.vue";

import { ConfirmDialogueMessage, PanelType } from "@/types";
import { appModule } from "@/store";
import GenericConfirmDialog from "@/components/common/modals/AppConfirmModal.vue";

export default Vue.extend({
  name: "App",
  components: {
    GenericConfirmDialog,
    AppBar,
    Snackbar,
    LeftNavDrawer,
    RightNavDrawer,
    ArtifactCreator,
  },
  computed: {
    isLeftOpen(): boolean {
      return appModule.getIsLeftOpen;
    },
    isRightOpen(): boolean {
      return appModule.getIsRightOpen;
    },
    isArtifactCreatorOpen(): boolean {
      return appModule.getIsArtifactCreatorOpen;
    },
    confirmationMessage(): ConfirmDialogueMessage | undefined {
      return appModule.getConfirmationMessage;
    },
  },
  methods: {
    closeArtifactCreator(): void {
      appModule.closePanel(PanelType.artifactCreator);
    },
  },
});
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400&display=swap");
@import "./assets/app-styles.css";
@import "./assets/artifact-styles.css";
@import "./assets/context-menu.css";
@import "./assets/modal-sizes.css";
</style>

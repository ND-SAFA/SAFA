<template>
  <v-app class="application">
    <v-main>
      <transition name="fade" mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </transition>
    </v-main>

    <AppBar
      v-if="doShowNavigation"
      :isLeftOpen="isLeftOpen"
      :isRightOpen="isRightOpen"
    />
    <LeftNavDrawer
      v-if="doShowNavigation"
      :isLeftOpen="isLeftOpen"
      :width="250"
    />
    <RightNavDrawer
      v-if="doShowNavigation"
      :isRightOpen="isRightOpen"
      :width="325"
    />

    <ArtifactCreatorModal
      :isOpen="isArtifactCreatorOpen"
      @onClose="closeArtifactCreator"
    />
    <AppConfirmModal :message="confirmationMessage" />
    <Snackbar :timeout="5000" />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { ConfirmDialogueMessage, PanelType } from "@/types/store";
import { appModule, sessionModule } from "@/store";
import {
  AppBar,
  Snackbar,
  LeftNavDrawer,
  RightNavDrawer,
  ArtifactCreatorModal,
  AppConfirmModal,
} from "@/components";

export default Vue.extend({
  name: "App",
  components: {
    AppConfirmModal,
    AppBar,
    Snackbar,
    LeftNavDrawer,
    RightNavDrawer,
    ArtifactCreatorModal,
  },
  computed: {
    isLeftOpen: () => appModule.getIsLeftOpen,
    isRightOpen: () => appModule.getIsRightOpen,
    isArtifactCreatorOpen: () => appModule.getIsArtifactCreatorOpen,
    confirmationMessage: () => appModule.getConfirmationMessage,
    doShowNavigation: () => sessionModule.getDoesSessionExist,
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

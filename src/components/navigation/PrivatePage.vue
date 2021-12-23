<template>
  <v-container :class="fullWindow ? 'full-window-page' : ''">
    <slot name="page" />
    <app-bar :is-left-open="isLeftOpen" :is-right-open="isRightOpen" />
    <left-nav-drawer :is-left-open="isLeftOpen" :width="250" />
    <right-nav-drawer :is-right-open="isRightOpen" :width="325" />
    <artifact-creator-modal
      :is-open="isArtifactCreatorOpen"
      @close="closeArtifactCreator"
    />
    <AppConfirmModal :message="confirmationMessage" />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appModule, logModule } from "@/store";
import { LeftNavDrawer, RightNavDrawer } from "@/components/side-panels";
import { AppConfirmModal, ArtifactCreatorModal } from "@/components/common";
import AppBar from "./AppBar.vue";

export default Vue.extend({
  name: "private-page",
  components: {
    AppBar,
    LeftNavDrawer,
    RightNavDrawer,
    ArtifactCreatorModal,
    AppConfirmModal,
  },
  props: {
    fullWindow: Boolean,
  },
  computed: {
    isLeftOpen: () => appModule.getIsLeftOpen,
    isRightOpen: () => appModule.getIsRightOpen,
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

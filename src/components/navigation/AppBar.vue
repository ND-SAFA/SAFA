<template>
  <v-app-bar app clipped-right clipped-left color="primary">
    <v-flex>
      <app-bar-header />
      <v-divider class="blue-grey" v-if="doShowGraphButtons" />
      <loading-bar v-if="!doShowGraphButtons" />
    </v-flex>

    <template v-slot:extension v-if="doShowGraphButtons">
      <v-row dense class="pt-1 full-width">
        <v-col cols="8">
          <div class="d-flex flex-row">
            <generic-icon-button
              color="secondary"
              :tooltip="leftPanelTooltip"
              :icon-id="leftPanelIcon"
              @click="handleLeftPanelClick"
            />
            <document-selector />
            <graph-buttons />
          </div>
        </v-col>
        <v-col cols="4">
          <v-row justify="end" class="ma-0 pa-0">
            <generic-icon-button
              color="secondary"
              :tooltip="rightPanelTooltip"
              :icon-id="rightPanelIcon"
              @click="handleRightPanelClick"
            />
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <loading-bar />
      </v-row>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule, documentModule } from "@/store";
import { router, Routes } from "@/router";
import { GenericIconButton } from "@/components/common";
import { AppBarHeader, GraphButtons } from "./header";
import { DocumentSelector } from "./document";
import LoadingBar from "./LoadingBar.vue";

/**
 * Displays the navigation top bar.
 */
export default Vue.extend({
  name: "AppBar",
  components: {
    DocumentSelector,
    GraphButtons,
    AppBarHeader,
    GenericIconButton,
    LoadingBar,
  },
  computed: {
    /**
     * @return Whether the left panel is open.
     */
    isLeftOpen: () => appModule.getIsLeftOpen,
    /**
     * @return Whether the right panel is open.
     */
    isRightOpen: () => appModule.getIsRightOpen,
    /**
     * @return Whether to display graphing buttons.
     */
    doShowGraphButtons(): boolean {
      return router.currentRoute.path === Routes.ARTIFACT;
    },
    /**
     * @return Whether to disable graphing buttons.
     */
    doDisableButtons(): boolean {
      return documentModule.isTableDocument;
    },
    /**
     * @return The left panel button icon to display.
     */
    leftPanelIcon(): string {
      return this.isLeftOpen ? "mdi-arrow-left" : "mdi-information-outline";
    },
    /**
     * @return The left panel button tooltip to display.
     */
    leftPanelTooltip(): string {
      return this.isLeftOpen
        ? "Close Artifact Details"
        : "Open Artifact Details";
    },
    /**
     * @return The right panel button icon to display.
     */
    rightPanelIcon(): string {
      return this.isRightOpen ? "mdi-arrow-right" : "mdi-family-tree";
    },
    /**
     * @return The right panel button tooltip to display.
     */
    rightPanelTooltip(): string {
      return this.isRightOpen ? "Close Graph Options" : "Open Graph Options";
    },
  },
  methods: {
    /**
     * Toggles the left panel.
     */
    handleLeftPanelClick() {
      appModule.toggleLeftPanel();
    },
    /**
     * Toggles the right panel.
     */
    handleRightPanelClick() {
      appModule.toggleRightPanel();
    },
  },
});
</script>

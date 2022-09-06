<template>
  <v-app-bar app clipped-right clipped-left color="primary">
    <v-flex>
      <app-bar-header />
      <v-divider class="white faded mt-1" v-if="doShowGraphButtons" />
      <loading-bar v-if="!doShowGraphButtons" />
    </v-flex>

    <template v-slot:extension v-if="doShowGraphButtons">
      <v-row dense class="full-width">
        <v-col cols="8">
          <flex-box>
            <generic-icon-button
              color="white"
              :tooltip="leftPanelTooltip"
              :icon-id="leftPanelIcon"
              data-cy="button-left-panel-toggle"
              @click="handleLeftPanelClick"
            />
            <document-selector />
            <graph-buttons />
            <searchbar />
          </flex-box>
        </v-col>
        <v-col cols="4">
          <flex-box justify="end">
            <generic-icon-button
              color="white"
              :tooltip="rightPanelTooltip"
              :icon-id="rightPanelIcon"
              data-cy="button-right-panel-toggle"
              @click="handleRightPanelClick"
            />
          </flex-box>
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
import { Route } from "vue-router";
import { appStore, documentStore } from "@/hooks";
import { router, Routes } from "@/router";
import { GenericIconButton, FlexBox } from "@/components/common";
import LoadingBar from "./LoadingBar.vue";
import { DocumentSelector } from "./document";
import { AppBarHeader, GraphButtons, Searchbar } from "./header";

/**
 * Displays the navigation top bar.
 */
export default Vue.extend({
  name: "AppBar",
  components: {
    FlexBox,
    Searchbar,
    DocumentSelector,
    GraphButtons,
    AppBarHeader,
    GenericIconButton,
    LoadingBar,
  },
  data() {
    return {
      doShowGraphButtons: router.currentRoute.path === Routes.ARTIFACT,
    };
  },
  watch: {
    /**
     * Checks whether the graph buttons should be visible when the route changes.
     */
    $route(to: Route) {
      this.doShowGraphButtons = to.path === Routes.ARTIFACT;
    },
  },
  computed: {
    /**
     * @return Whether the left panel is open.
     */
    isLeftOpen: () => appStore.isLeftPanelOpen,
    /**
     * @return Whether the right panel is open.
     */
    isRightOpen: () => appStore.isRightPanelOpen,
    /**
     * @return Whether to disable graphing buttons.
     */
    doDisableButtons(): boolean {
      return documentStore.isTableDocument;
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
      appStore.toggleLeftPanel();
    },
    /**
     * Toggles the right panel.
     */
    handleRightPanelClick() {
      appStore.toggleRightPanel();
    },
  },
});
</script>

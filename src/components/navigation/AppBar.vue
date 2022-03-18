<template>
  <v-app-bar app clipped-right clipped-left color="primary">
    <v-flex>
      <app-bar-header />
      <v-divider class="blue-grey" v-if="doShowGraphButtons" />
      <loading-bar v-if="!doShowGraphButtons" :isLoading="isLoading" />
    </v-flex>

    <template v-slot:extension v-if="doShowGraphButtons">
      <v-row dense class="pt-1 full-width">
        <v-col cols="4">
          <v-row dense align="center">
            <v-col class="flex-grow-0">
              <generic-icon-button
                color="secondary"
                :tooltip="leftPanelTooltip"
                :icon-id="
                  isLeftOpen ? 'mdi-arrow-left' : 'mdi-information-outline'
                "
                :is-disabled="doDisableButtons"
                @click="onLeftPanelClick"
              />
            </v-col>
            <v-col>
              <document-selector />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="4">
          <graph-buttons />
        </v-col>
        <v-col cols="4">
          <v-row justify="end" class="ma-0 pa-0">
            <generic-icon-button
              color="secondary"
              :tooltip="rightPanelTooltip"
              :icon-id="isRightOpen ? 'mdi-arrow-right' : 'mdi-family-tree'"
              :is-disabled="doDisableButtons"
              @click="onRightPanelClick"
            />
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <loading-bar :isLoading="isLoading" />
      </v-row>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule, documentModule } from "@/store";
import { GenericIconButton } from "@/components/common";
import { router, Routes } from "@/router";
import AppBarHeader from "./header/AppBarHeader.vue";
import GraphButtons from "./graph/GraphButtons.vue";
import LoadingBar from "./LoadingBar.vue";
import DocumentSelector from "./document/DocumentSelector.vue";

export default Vue.extend({
  components: {
    DocumentSelector,
    GraphButtons,
    AppBarHeader,
    GenericIconButton,
    LoadingBar,
  },
  props: {
    isLeftOpen: Boolean,
    isRightOpen: Boolean,
  },
  computed: {
    doShowGraphButtons(): boolean {
      return router.currentRoute.path === Routes.ARTIFACT;
    },
    doDisableButtons(): boolean {
      return documentModule.isTableDocument;
    },
    isLoading(): boolean {
      return appModule.getIsLoading;
    },
    leftPanelTooltip(): string {
      return this.isLeftOpen
        ? "Close Artifact Details"
        : "Open Artifact Details";
    },
    rightPanelTooltip(): string {
      return this.isRightOpen ? "Close Graph Options" : "Open Graph Options";
    },
  },
  methods: {
    onLeftPanelClick() {
      appModule.toggleLeftPanel();
    },
    onRightPanelClick() {
      appModule.toggleRightPanel();
    },
  },
});
</script>

<style scoped>
.divider-theme {
  border-right: 1px solid grey;
}
</style>

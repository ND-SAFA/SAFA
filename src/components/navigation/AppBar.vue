<template>
  <v-app-bar app clipped-right clipped-left color="primary">
    <v-flex>
      <app-bar-header />
      <v-divider class="blue-grey" v-if="doShowGraphButtons" />
      <loading-bar v-if="!doShowGraphButtons" :isLoading="isLoading" />
    </v-flex>

    <template v-slot:extension v-if="doShowGraphButtons">
      <v-row class="pt-1" style="width: 100%">
        <v-col cols="4">
          <v-row dense align="center">
            <v-col class="flex-grow-0">
              <generic-icon-button
                color="secondary"
                :tooltip="leftPanelTooltip"
                :icon-id="
                  isLeftOpen ? 'mdi-arrow-left' : 'mdi-information-outline'
                "
                @click="onLeftPanelClick"
              />
            </v-col>
            <v-col>
              <document-selector />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="4">
          <graph-nav-icons />
        </v-col>
        <v-col cols="4">
          <v-row justify="end" class="ma-0 pa-0">
            <generic-icon-button
              color="secondary"
              :tooltip="rightPanelTooltip"
              :icon-id="isRightOpen ? 'mdi-arrow-right' : 'mdi-family-tree'"
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
import { appModule } from "@/store";
import { GenericIconButton } from "@/components/common";
import { router, Routes } from "@/router";
import AppBarHeader from "./AppBarHeader.vue";
import GraphNavIcons from "./GraphNavIcons.vue";
import LoadingBar from "./LoadingBar.vue";
import DocumentSelector from "@/components/navigation/DocumentSelector.vue";

export default Vue.extend({
  components: {
    DocumentSelector,
    GraphNavIcons,
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
      return router.currentRoute.path === Routes.ARTIFACT_TREE;
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

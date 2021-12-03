<template>
  <v-app-bar app clipped-right clipped-left color="primary">
    <v-flex>
      <AppBarHeader />
      <v-divider class="blue-grey" v-if="doShowGraphButtons" />
    </v-flex>

    <template v-slot:extension v-if="doShowGraphButtons">
      <v-container fluid class="ma-0 pa-0">
        <v-row>
          <v-col cols="4">
            <GenericIconButton
              color="secondary"
              :tooltip="leftPanelTooltip"
              :icon-id="
                isLeftOpen ? 'mdi-arrow-left' : 'mdi-information-outline'
              "
              @click="onLeftPanelClick"
            />
          </v-col>
          <v-col cols="4">
            <GraphNavIcons />
          </v-col>
          <v-col cols="4">
            <v-row justify="end" class="ma-0 pa-0">
              <GenericIconButton
                color="secondary"
                :tooltip="rightPanelTooltip"
                :icon-id="isRightOpen ? 'mdi-arrow-right' : 'mdi-family-tree'"
                @click="onRightPanelClick"
              />
            </v-row>
          </v-col>
        </v-row>
        <v-row>
          <v-progress-linear
            rounded
            height="5"
            v-show="isLoading"
            indeterminate
            absolute
            bottom
            color="secondary"
          />
        </v-row>
      </v-container>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule } from "@/store";
import { GenericIconButton } from "@/components/common";
import AppBarHeader from "./AppBarHeader.vue";
import GraphNavIcons from "./GraphNavIcons.vue";
import { router, Routes } from "@/router";

export default Vue.extend({
  components: {
    GraphNavIcons,
    AppBarHeader,
    GenericIconButton,
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

<template>
  <v-app-bar app extended clipped-right clipped-left color="primary">
    <v-container fluid class="ma-0 pa-0">
      <AppBarHeader />
      <v-divider light style="border-top: 1px solid grey" />
    </v-container>
    <template v-slot:extension class="ma-0 pa-0">
      <v-container fluid class="ma-0 pa-0">
        <v-row>
          <v-col cols="4">
            <GenericIconButton
              :tooltip="leftPanelTooltip"
              color="secondary"
              @onClick="onLeftPanelClick"
              :icon-id="
                isLeftOpen ? 'mdi-arrow-left' : 'mdi-information-outline'
              "
            />
          </v-col>
          <v-col cols="4">
            <GraphNavIcons />
          </v-col>
          <v-col cols="4">
            <v-row justify="end" class="ma-0 pa-0">
              <GenericIconButton
                :tooltip="rightPanelTooltip"
                color="secondary"
                @onClick="onRightPanelClick"
                :iconId="isRightOpen ? 'mdi-arrow-right' : 'mdi-family-tree'"
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
import { GenericIconButton } from "@/components";
import AppBarHeader from "./AppBarHeader.vue";
import GraphNavIcons from "./GraphNavIcons.vue";

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
    isLoading(): boolean {
      return appModule.getIsLoading;
    },
    leftPanelTooltip(): string {
      return this.isLeftOpen
        ? "Close artifact details"
        : "Open artifact details";
    },
    rightPanelTooltip(): string {
      return this.isRightOpen ? "Close graph options" : "Open graph options";
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

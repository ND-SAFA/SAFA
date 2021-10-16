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
            <v-btn text small color="secondary" @click="onLeftPanelClick">
              <v-icon v-if="isLeftOpen">mdi-arrow-left</v-icon>
              <v-icon v-else>mdi-information-outline</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4">
            <GraphNavIcons />
          </v-col>
          <v-col cols="4">
            <v-row justify="end" class="ma-0 pa-0">
              <v-btn text small color="secondary" @click="onRightPanelClick">
                <v-icon v-if="isRightOpen">mdi-arrow-right</v-icon>
                <v-icon v-else>mdi-family-tree</v-icon>
              </v-btn>
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
import GraphNavIcons from "@/components/navigation/GraphNavIcons.vue";
import AppBarHeader from "@/components/navigation//AppBarHeader.vue";
import { appModule } from "@/store";

export default Vue.extend({
  components: {
    GraphNavIcons,
    AppBarHeader,
  },
  props: {
    isLeftOpen: Boolean,
    isRightOpen: Boolean,
  },
  computed: {
    isLoading(): boolean {
      return appModule.isLoading;
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

<template>
  <v-container>
    <v-row>
      <v-tabs centered v-model="selectedTab">
        <v-tab>Hierarchy</v-tab>
        <v-tab>Delta</v-tab>
        <v-tab>Types</v-tab>
        <v-tab>Safety</v-tab>
      </v-tabs>
    </v-row>

    <v-expansion-panels multiple>
      <sub-tree-selector-tab v-if="selectedTab === 0" />
      <delta-tab v-if="selectedTab === 1" @open="openDeltaPanel" />
      <trace-link-direction-tab v-if="selectedTab === 2" />
      <safety-notation-tab v-if="selectedTab === 3" />
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SubTreeSelectorTab from "./SubTreeSelectorTab.vue";
import DeltaTab from "./DeltaTab.vue";
import SafetyNotationTab from "./SafetyNotationTab.vue";
import TraceLinkDirectionTab from "./TypeOptionsTab.vue";

const DELTA_TREE_INDEX = 1;

export default Vue.extend({
  name: "hazard-hierarchy-panel",
  components: {
    TraceLinkDirectionTab,
    SafetyNotationTab,
    DeltaTab,
    SubTreeSelectorTab,
  },
  data() {
    return {
      selectedTab: -1,
    };
  },
  methods: {
    openDeltaPanel(): void {
      this.selectedTab = DELTA_TREE_INDEX;
    },
  },
});
</script>

<template>
  <v-container>
    <v-row>
      <v-tabs centered v-model="selectedTab" show-arrows>
        <v-tab>Sub Tree Selector</v-tab>
        <v-tab>Delta</v-tab>
        <v-tab>Safety Notation</v-tab>
      </v-tabs>
    </v-row>

    <v-expansion-panels multiple>
      <SubTreeSelectorTab v-if="selectedTab === 0" />
      <DeltaTab v-if="selectedTab === 1" @open="openDeltaPanel" />
      <SafetyNotationTab v-if="selectedTab === 2" />
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SubTreeSelectorTab from "./SubTreeSelectorTab.vue";
import DeltaTab from "./DeltaTab.vue";
import SafetyNotationTab from "./SafetyNotationTab.vue";

const DELTA_TREE_INDEX = 1;

export default Vue.extend({
  name: "hazard-hierarchy-panel",
  components: {
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

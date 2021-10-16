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
      <DeltaPanel v-if="selectedTab === 1" @open="openDeltaPanel" />
      <SafetyNotationPanel v-if="selectedTab === 2" />
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SafetyNotationPanel from "@/components/side-panels/right/SafetyNotationTab.vue";
import DeltaPanel from "@/components/side-panels/right/DeltaTab.vue";
import SubTreeSelectorTab from "@/components/side-panels/right/SubTreeSelectorTab.vue";

const DELTA_TREE_INDEX = 1;

export default Vue.extend({
  name: "hazard-hierarchy-panel",
  components: {
    SafetyNotationPanel,
    DeltaPanel,
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

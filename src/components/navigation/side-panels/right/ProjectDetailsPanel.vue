<template>
  <v-container>
    <v-row>
      <v-tabs centered v-model="selectedTab">
        <v-tab>Hierarchy</v-tab>
        <v-tab>Delta</v-tab>
        <v-tab>Types</v-tab>
      </v-tabs>
    </v-row>

    <v-expansion-panels multiple>
      <sub-tree-selector-tab v-if="selectedTab === 0" />
      <delta-tab v-if="selectedTab === 1" />
      <trace-link-direction-tab v-if="selectedTab === 2" />
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SubTreeSelectorTab from "./SubTreeSelectorTab.vue";
import DeltaTab from "./DeltaTab.vue";
import TraceLinkDirectionTab from "./TypeOptionsTab.vue";

/**
 * Displays the project details panel.
 */
export default Vue.extend({
  name: "ProjectDetailsPanel",
  components: {
    TraceLinkDirectionTab,
    DeltaTab,
    SubTreeSelectorTab,
  },
  data() {
    return {
      selectedTab: -1,
    };
  },
});
</script>

<template>
  <v-container>
    <settings-overview />
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <settings-members />
      </v-tab-item>
      <v-tab-item key="2"> </v-tab-item>
      <v-tab-item key="3"> </v-tab-item>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { settingsTabOptions } from "@/util";
import { TabList } from "@/components/common";
import SettingsOverview from "./SettingsOverview.vue";
import SettingsMembers from "./SettingsMembers.vue";

/**
 * Tabs for changing project settings.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: { TabList, SettingsOverview, SettingsMembers },
  props: {},
  data() {
    return {
      tab: 0,
      tabs: settingsTabOptions(),
    };
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>

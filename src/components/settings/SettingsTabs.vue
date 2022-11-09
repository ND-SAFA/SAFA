<template>
  <v-container>
    <settings-header />
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <settings-overview />
      </v-tab-item>
      <v-tab-item key="2">
        <upload-new-version :is-open="tab === 2" />
      </v-tab-item>
      <v-tab-item key="3">
        <type-options />
      </v-tab-item>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { settingsTabOptions } from "@/util";
import { TabList } from "@/components/common";
import { UploadNewVersion } from "@/components/project/selector";
import SettingsHeader from "./SettingsHeader.vue";
import SettingsOverview from "./SettingsOverview.vue";
import TypeOptions from "./TypeOptions.vue";

/**
 * Tabs for changing project settings.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    TypeOptions,
    UploadNewVersion,
    TabList,
    SettingsOverview,
    SettingsHeader,
  },
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

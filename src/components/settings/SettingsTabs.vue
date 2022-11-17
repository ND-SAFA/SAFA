<template>
  <sidebar-grid>
    <template v-slot:header>
      <settings-header />
    </template>
    <template v-slot:sidebar>
      <project-buttons />
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <settings-members />
      </v-tab-item>
      <v-tab-item key="2">
        <upload-new-version :is-open="tab === 2" />
      </v-tab-item>
      <v-tab-item key="3">
        <project-installations-table />
      </v-tab-item>
      <v-tab-item key="4">
        <type-options />
      </v-tab-item>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
import Vue from "vue";
import { settingsTabOptions } from "@/util";
import { TabList, SidebarGrid } from "@/components/common";
import {
  UploadNewVersion,
  ProjectButtons,
  ProjectDisplay,
} from "@/components/project";
import { ProjectInstallationsTable } from "@/components/integrations";
import SettingsHeader from "./SettingsHeader.vue";
import TypeOptions from "./TypeOptions.vue";
import { SettingsMembers } from "./members";

/**
 * Tabs for changing project settings.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    ProjectInstallationsTable,
    SidebarGrid,
    ProjectDisplay,
    ProjectButtons,
    TypeOptions,
    UploadNewVersion,
    TabList,
    SettingsMembers,
    SettingsHeader,
  },
  data() {
    return {
      tab: 0,
      tabs: settingsTabOptions(),
    };
  },
});
</script>

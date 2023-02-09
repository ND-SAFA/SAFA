<template>
  <sidebar-grid>
    <template #header>
      <settings-header />
    </template>
    <template #sidebar>
      <project-buttons />
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab key="1">
        <settings-members />
      </v-tab>
      <v-tab key="2">
        <upload-new-version :is-open="tab === 2" />
      </v-tab>
      <v-tab key="3">
        <project-installations-table />
      </v-tab>
      <v-tab key="4">
        <attribute-settings />
      </v-tab>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
import Vue from "vue";
import { SelectOption } from "@/types";
import { settingsTabOptions } from "@/util";
import { projectStore, sessionStore } from "@/hooks";
import { TabList, SidebarGrid } from "@/components/common";
import {
  UploadNewVersion,
  ProjectButtons,
  ProjectDisplay,
} from "@/components/project";
import { ProjectInstallationsTable } from "@/components/integrations";
import { AttributeSettings } from "@/components/attributes";
import SettingsHeader from "./SettingsHeader.vue";
import { SettingsMembers } from "./members";

/**
 * Tabs for changing project settings.
 */
export default Vue.extend({
  name: "TracePredictionTabs",
  components: {
    AttributeSettings,
    ProjectInstallationsTable,
    SidebarGrid,
    ProjectDisplay,
    ProjectButtons,
    UploadNewVersion,
    TabList,
    SettingsMembers,
    SettingsHeader,
  },
  data() {
    return {
      tab: 0,
    };
  },
  computed: {
    /**
     * @return The tabs to display.
     */
    tabs(): SelectOption[] {
      return sessionStore.isEditor(projectStore.project)
        ? settingsTabOptions()
        : [settingsTabOptions()[0]];
    },
  },
});
</script>

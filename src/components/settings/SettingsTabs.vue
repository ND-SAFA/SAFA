<template>
  <sidebar-grid>
    <template #sidebar>
      <project-buttons />
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #members>
        <project-member-table />
      </template>
      <template #upload>
        <upload-new-version :open="tab === 'upload'" />
      </template>
      <template #integrations>
        <project-installations-table />
      </template>
      <template #attributes>
        <attribute-settings />
      </template>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
/**
 * Tabs for changing project settings.
 */
export default {
  name: "TracePredictionTabs",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { SettingsTabTypes } from "@/types";
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
import { ProjectMemberTable } from "./members";

const tab = ref(SettingsTabTypes.members);

const tabs = computed(() =>
  sessionStore.isEditor(projectStore.project)
    ? settingsTabOptions()
    : [settingsTabOptions()[0]]
);
</script>

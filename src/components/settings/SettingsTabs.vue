<template>
  <sidebar-grid>
    <template #sidebar>
      <project-buttons />
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #members>
        <member-table variant="project" />
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
  name: "SettingsTabs",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { SettingsTabTypes } from "@/types";
import { settingsTabOptions } from "@/util";
import { permissionStore } from "@/hooks";
import { TabList, SidebarGrid } from "@/components/common";
import {
  UploadNewVersion,
  ProjectButtons,
  ProjectDisplay,
} from "@/components/project";
import { ProjectInstallationsTable } from "@/components/integrations";
import { AttributeSettings } from "@/components/attributes";
import { MemberTable } from "@/components/members";

const tab = ref(SettingsTabTypes.members);

const tabs = computed(() =>
  permissionStore.projectAllows("editor")
    ? settingsTabOptions()
    : [settingsTabOptions()[0]]
);
</script>

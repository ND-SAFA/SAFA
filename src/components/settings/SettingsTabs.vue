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
  name: "SettingsTabs",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { SelectOption, SettingsTabTypes } from "@/types";
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
import { ProjectMemberTable } from "@/components/members";

const tab = ref(SettingsTabTypes.members);

const tabs = computed(() => {
  const options = settingsTabOptions();
  const visibleOptions: SelectOption[] = [options[0]];

  if (permissionStore.isAllowed("project.edit_versions")) {
    visibleOptions.push(options[1]);
  } else if (permissionStore.isAllowed("project.edit_integrations")) {
    visibleOptions.push(options[2]);
  } else if (permissionStore.isAllowed("project.edit")) {
    visibleOptions.push(options[3]);
  }

  return visibleOptions;
});
</script>

<template>
  <sidebar-grid>
    <template #sidebar>
      <project-buttons />
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #overview>
        <project-overview-display hide-title />
      </template>
      <template #members>
        <project-member-table />
      </template>
      <template #jobs>
        <jobs-table :display-project-jobs="true" />
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
import { SelectOption } from "@/types";
import { settingsTabOptions } from "@/util";
import { permissionStore } from "@/hooks";
import { TabList, SidebarGrid } from "@/components/common";
import {
  UploadNewVersion,
  ProjectButtons,
  ProjectDisplay,
  ProjectOverviewDisplay,
} from "@/components/project";
import { ProjectInstallationsTable } from "@/components/integrations";
import { AttributeSettings } from "@/components/attributes";
import { ProjectMemberTable } from "@/components/members";
import { JobsTable } from "@/components/jobs";

const tabs = computed(() => {
  const options = settingsTabOptions();
  const visibleOptions: SelectOption[] = [options[0], options[1]];

  if (permissionStore.isAllowed("project.edit_versions")) {
    visibleOptions.push(options[2], options[3]);
  }
  if (permissionStore.isAllowed("project.edit_integrations")) {
    visibleOptions.push(options[4]);
  }
  if (permissionStore.isAllowed("project.edit")) {
    visibleOptions.push(options[5]);
  }

  return visibleOptions;
});
const tab = ref(tabs.value[0].id);
</script>

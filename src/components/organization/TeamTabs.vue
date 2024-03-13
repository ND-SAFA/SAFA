<template>
  <sidebar-grid>
    <template #sidebar>
      <team-buttons />
      <team-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #members>
        <team-member-table />
      </template>
      <template #projects>
        <project-version-stepper team-only />
      </template>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
/**
 * Tabs for changing team settings.
 */
export default {
  name: "TeamTabs",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { teamTabTypes } from "@/util";
import { TabList, SidebarGrid } from "@/components/common";
import { TeamButtons, TeamDisplay } from "@/components/organization/save";
import { TeamMemberTable } from "@/components/members";
import { ProjectVersionStepper } from "@/components/project";

const tabs = teamTabTypes();

const tab = ref(tabs[0].id);
</script>

<template>
  <sidebar-grid>
    <template #sidebar>
      <organization-buttons />
      <organization-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #members>
        <member-table variant="organization" />
      </template>
      <template #teams>
        <team-tab />
      </template>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
/**
 * Tabs for changing organization settings.
 */
export default {
  name: "OrganizationTabs",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { OrganizationTabTypes } from "@/types";
import { organizationTabTypes } from "@/util";
import { TabList, SidebarGrid } from "@/components/common";
import {
  OrganizationButtons,
  OrganizationDisplay,
} from "@/components/organization/save";
import { MemberTable } from "@/components/members";
import { TeamTab } from "@/components/organization/team";

const tabs = organizationTabTypes();

const tab = ref(OrganizationTabTypes.members);
</script>

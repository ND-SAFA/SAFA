<template>
  <sidebar-grid>
    <template #sidebar>
      <organization-buttons />
      <organization-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #members>
        <panel-card
          title="Members"
          subtitle="Manage organization members and permissions."
        >
        </panel-card>
      </template>
      <template #teams>
        <panel-card title="Teams" subtitle="Manage teams and permissions.">
        </panel-card>
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
import { TabList, SidebarGrid, PanelCard } from "@/components/common";
import {
  OrganizationButtons,
  OrganizationDisplay,
} from "@/components/organization/display";

const tabs = organizationTabTypes();

const tab = ref(OrganizationTabTypes.members);
</script>

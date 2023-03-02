<template>
  <sidebar-grid>
    <template #sidebar>
      <project-display />
    </template>
    <tab-list v-model="tab" :tabs="tabs">
      <template #models>
        <model-table />
      </template>
      <template #generation>
        <panel-card>
          <trace-link-generator :is-open="tab === 'generation'" />
        </panel-card>
      </template>
      <template #approval>
        <trace-approval-table />
      </template>
    </tab-list>
  </sidebar-grid>
</template>

<script lang="ts">
/**
 * Tabs for predicting and approving trace links.
 */
export default {
  name: "TracePredictionTabs",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { TracePredictionTabTypes } from "@/types";
import { tracePredictionTabOptions } from "@/util";
import { TabList, SidebarGrid, PanelCard } from "@/components/common";
import { TraceLinkGenerator } from "@/components/traceLink";
import { ProjectDisplay } from "@/components/project";
import { ModelTable } from "./training";
import { TraceApprovalTable } from "./approval";

const tabs = tracePredictionTabOptions();

const tab = ref<TracePredictionTabTypes>(TracePredictionTabTypes.models);
</script>

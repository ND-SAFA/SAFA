<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template #standard>
      <project-creator-stepper />
    </template>
    <template #bulk>
      <project-bulk-upload />
    </template>
    <template #import>
      <integrations-stepper type="create" />
    </template>
  </tab-list>
</template>

<script lang="ts">
/**
 * Allows for creating a project.
 */
export default {
  name: "ProjectCreator",
};
</script>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { creatorTabOptions } from "@/util";
import { getParam, QueryParams, updateParam } from "@/router";
import { TabList } from "@/components/common";
import { IntegrationsStepper } from "@/components/integrations";
import { ProjectCreatorStepper, ProjectBulkUpload } from "./workflows";

const tabs = creatorTabOptions();
const tab = ref(tabs[0].id);
const currentRoute = useRoute();

/**
 * Switch to any set tab in the query.
 */
function openCurrentTab() {
  const tabId = getParam(QueryParams.TAB);
  const navTab = tabs.find(({ id }) => id === tabId);

  if (!tabId || !navTab || navTab.id === tab.value) return;

  tab.value = navTab.id;
}

onMounted(() => openCurrentTab());

watch(
  () => currentRoute.path,
  () => openCurrentTab()
);

watch(
  () => tab.value,
  (currentTabId) => {
    const routeTabId = getParam(QueryParams.TAB);

    if (currentTabId !== routeTabId) {
      updateParam(QueryParams.TAB, currentTabId);
    }
  }
);
</script>

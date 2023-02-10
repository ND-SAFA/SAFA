<template>
  <v-container>
    <typography t="4" el="h1" variant="title" value="Create Project" />
    <v-divider />
    <typography
      el="p"
      y="2"
      value="Create a project using one of the following methods."
    />
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab key="1">
        <project-creator-stepper />
      </v-tab>
      <v-tab key="2">
        <project-bulk-upload />
      </v-tab>
      <v-tab key="3">
        <integrations-stepper type="create" />
      </v-tab>
    </tab-list>
  </v-container>
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
import { TabList, Typography } from "@/components/common";
import { IntegrationsStepper } from "@/components/integrations";
import { ProjectCreatorStepper, ProjectBulkUpload } from "./workflows";

const tabs = creatorTabOptions();
const tab = ref(0);
const currentRoute = useRoute();

/**
 * Switch to any set tab in the query.
 */
function openCurrentTab() {
  const tabId = getParam(QueryParams.TAB);
  const tabIndex = tabs.findIndex(({ id }) => id === tabId);

  if (!tabId || tabIndex === -1 || tab.value === tabIndex) return;

  tab.value = tabIndex;
}

onMounted(() => openCurrentTab());

watch(
  () => currentRoute.path,
  () => openCurrentTab()
);

watch(
  () => tab.value,
  (index) => {
    const currentTabId = tabs[index].id;
    const routeTabId = getParam(QueryParams.TAB);

    if (currentTabId !== routeTabId) {
      updateParam(QueryParams.TAB, currentTabId);
    }
  }
);
</script>

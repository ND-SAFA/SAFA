<template>
  <flex-box :column="smallWindow" justify="center">
    <flex-item
      :parts="smallWindow ? '12' : '6'"
      :class="smallWindow ? 'full-width' : ''"
    >
      <panel-card
        class="q-ma-sm"
        title="Create New Project"
        subtitle="Import collections of code files, documents, or other artifacts."
      >
        <flex-box :column="smallWindow" full-width>
          <tab-list v-model="tab" :tabs="tabs" :vertical="!smallWindow">
            <template #name>
              <project-identifier-input
                v-model:name="identifier.name"
                v-model:description="identifier.description"
              />
              <text-button
                block
                outlined
                :disabled="continueDisabled"
                label="Import Data"
                color="primary"
                class="q-mt-md"
                icon="upload"
                data-cy="button-continue-project"
                @click="tab = 'data'"
              />
            </template>
            <template #data>
              <upload-panel-list />
              <text-button
                :disabled="uploadDisabled"
                block
                label="Create Project"
                color="primary"
                class="q-mt-md"
                icon="project-add"
                data-cy="button-create-project"
                @click="handleCreate"
              />
            </template>
          </tab-list>
        </flex-box>
      </panel-card>
    </flex-item>
    <flex-item :parts="smallWindow ? '12' : '6'" :class="graphClassName">
      <panel-card>
        <creator-tree />
      </panel-card>
    </flex-item>
  </flex-box>
</template>

<script lang="ts">
/**
 * Builds project data uploads from all data sources.
 */
export default {
  name: "ProjectBuilder",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { CreatorSectionTab, CreatorTab, UploadPanelType } from "@/types";
import { creatorTabOptions } from "@/util";
import {
  createProjectApiStore,
  gitHubApiStore,
  identifierSaveStore,
  integrationsStore,
  jiraApiStore,
  projectSaveStore,
  useScreen,
} from "@/hooks";
import { getParam, QueryParams, Routes } from "@/router";
import {
  FlexBox,
  FlexItem,
  PanelCard,
  TextButton,
  TabList,
} from "@/components/common";
import { CreatorTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/save";
import { UploadPanelList } from "@/components/project/creator/upload";

const { smallWindow } = useScreen();
const currentRoute = useRoute();

const tabs = creatorTabOptions();
const tab = ref<CreatorSectionTab>("name");

const identifier = computed(() => identifierSaveStore.editedIdentifier);

const uploadMode = computed(() => projectSaveStore.mode);

const continueDisabled = computed(() => !identifierSaveStore.canSave);

const uploadDisabled = computed(
  () =>
    !projectSaveStore.uploadPanels
      .map(({ valid }) => valid)
      .reduce((acc, cur) => acc && cur, true) ||
    (!identifier.value.name && !["github", "jira"].includes(uploadMode.value))
);

const displayGraph = computed(() => projectSaveStore.graphNodes.length > 0);

const graphClassName = computed(() => {
  const graphClass = displayGraph.value
    ? "artifact-view visible q-ma-sm "
    : "artifact-view collapsed q-ma-sm ";
  const screenClass = smallWindow.value ? "full-width" : "";

  return graphClass + screenClass;
});

/**
 * Clears all project data.
 */
function handleClear() {
  identifierSaveStore.resetIdentifier(true);
  projectSaveStore.resetProject();
}

/**
 * Creates a new project.
 */
function handleCreate() {
  const callbacks = { onSuccess: handleClear };

  if (uploadMode.value === "bulk") {
    createProjectApiStore.handleBulkImport(
      identifier.value,
      projectSaveStore.uploadPanels[0]?.bulkFiles || [],
      projectSaveStore.uploadPanels[0]?.summarize || false,
      callbacks
    );
  } else if (uploadMode.value === "artifact" || uploadMode.value === "trace") {
    createProjectApiStore.handleImport(callbacks);
  } else if (uploadMode.value === "github") {
    createProjectApiStore.handleGitHubImport(callbacks);
  } else if (uploadMode.value === "jira") {
    createProjectApiStore.handleJiraImport(callbacks);
  }
}

/**
 * Reloads integrations data.
 */
function handleReloadIntegrations() {
  if (integrationsStore.validJiraCredentials) {
    jiraApiStore.handleLoadOrganizations();
  }
  if (integrationsStore.validGitHubCredentials) {
    gitHubApiStore.handleLoadProjects();
  }
}

/**
 * Reads the URL query for which tab to open to.
 */
function handleLoadTab() {
  const loadedToken = getParam(QueryParams.TAB);

  if (!loadedToken) return;

  const variant =
    (
      {
        standard: "artifact",
        bulk: "bulk",
        import: "github",
      } as Record<CreatorTab | string, UploadPanelType>
    )[String(loadedToken)] || "artifact";

  projectSaveStore.uploadPanels[0].variant = variant;

  tab.value = variant === "github" ? "data" : "name";
}

onMounted(() => handleReloadIntegrations());

watch(
  () => [
    integrationsStore.validJiraCredentials,
    integrationsStore.validGitHubCredentials,
  ],
  () => handleReloadIntegrations()
);

watch(
  () => currentRoute.path,
  (path) => {
    if (path !== Routes.PROJECT_CREATOR) return;

    handleClear();
    handleLoadTab();
  }
);

onMounted(handleLoadTab);
</script>

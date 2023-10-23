<template>
  <flex-box :column="smallWindow">
    <flex-item :parts="smallWindow ? '12' : '6'">
      <panel-card
        class="q-ma-sm"
        title="Create Project"
        subtitle="Create a new project by uploading files or configuring integrations."
      >
        <flex-box :column="smallWindow" full-width>
          <q-tabs v-model="tab" :vertical="!smallWindow" no-caps>
            <q-tab name="name" label="Project Details" />
            <q-tab name="data" label="Import Data" />
          </q-tabs>
          <separator vertical />
          <q-tab-panels
            v-model="tab"
            animated
            :vertical="!smallWindow"
            transition-prev="jump-up"
            transition-next="jump-up"
            class="full-width"
          >
            <q-tab-panel name="name">
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
                @click="tab = 'data'"
              />
            </q-tab-panel>
            <q-tab-panel name="data">
              <file-panel-list />
              <text-button
                :disabled="uploadDisabled"
                block
                label="Create Project"
                color="primary"
                class="q-mt-md"
                icon="project-add"
                @click="handleCreate"
              />
            </q-tab-panel>
          </q-tab-panels>
        </flex-box>
      </panel-card>
    </flex-item>
    <flex-item :parts="smallWindow ? '12' : '6'">
      <panel-card class="q-ma-sm">
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
import { computed, ref } from "vue";
import {
  createProjectApiStore,
  identifierSaveStore,
  projectSaveStore,
  useScreen,
} from "@/hooks";
import {
  FlexBox,
  FlexItem,
  PanelCard,
  Separator,
  TextButton,
} from "@/components/common";
import { CreatorTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/save";
import { FilePanelList } from "@/components/project/creator/files";

const { smallWindow } = useScreen();

const tab = ref("name");

const identifier = computed(() => identifierSaveStore.editedIdentifier);

const uploadMode = computed(() => projectSaveStore.uploadPanels[0]?.variant);

const continueDisabled = computed(() => !identifier.value.name);

const uploadDisabled = computed(
  () =>
    !projectSaveStore.uploadPanels
      .map(({ valid }) => valid)
      .reduce((acc, cur) => acc && cur, true)
);

/**
 * Clears all project data.
 */
function handleClear() {
  identifierSaveStore.resetIdentifier();
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
</script>

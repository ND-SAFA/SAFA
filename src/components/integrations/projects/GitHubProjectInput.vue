<template>
  <div>
    <git-hub-authentication v-if="!integrationsStore.validGitHubCredentials" />
    <select-input
      v-else
      v-model="integrationsStore.gitHubOrganization"
      label="GitHub Organization"
      :options="gitHubApiStore.organizationList"
      :loading="gitHubApiStore.loading"
      hint="Required"
      class="full-width"
      option-label="name"
      data-cy="input-github-organization"
    />
    <select-input
      v-if="!!integrationsStore.gitHubOrganization"
      v-model="integrationsStore.gitHubProject"
      label="GitHub Repository"
      :options="projects"
      hint="Required"
      class="full-width"
      option-label="name"
      data-cy="input-github-project"
    />
    <expansion-item
      v-if="!!integrationsStore.gitHubProject"
      label="Import Settings"
    >
      <flex-box v-if="!!projectName" column t="1">
        <flex-box y="1">
          <select-input
            v-model="importBranch"
            label="Import Branch"
            :options="branches"
            hint="The branch to import files from."
          />
          <text-input
            v-model="artifactType"
            label="Artifact Type"
            hint="A name for imported artifacts."
            class="q-mx-sm"
          />
        </flex-box>
        <flex-box y="1" align="center">
          <multiselect-input
            v-model="includePatterns"
            label="Include Patterns"
            :options="[]"
            add-values
            hint="Press enter to save a regex file path pattern."
          />
          <multiselect-input
            v-model="excludePatterns"
            label="Exclude Patterns"
            :options="[]"
            add-values
            hint="Press enter to save a regex file path pattern."
            class="q-mx-sm"
          />
          <icon-button
            tooltip="Learn about file patterns"
            icon="info"
            @click="handleFilePatternInfo"
          />
        </flex-box>
      </flex-box>
    </expansion-item>
  </div>
</template>

<script lang="ts">
/**
 * Allows for selecting a GitHub repository.
 */
export default {
  name: "GitHubProjectInput",
};
</script>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from "vue";
import { GitHubProjectSchema } from "@/types";
import { gitHubApiStore, integrationsStore } from "@/hooks";
import {
  FlexBox,
  SelectInput,
  MultiselectInput,
  TextInput,
  IconButton,
  ExpansionItem,
} from "@/components/common";
import { GitHubAuthentication } from "@/components/integrations/authentication";

const projects = ref<GitHubProjectSchema[]>([]);

const organizationName = computed(
  () => integrationsStore.gitHubOrganization?.name
);

const projectName = computed(() => integrationsStore.gitHubProject?.name);

const branches = computed(
  () => integrationsStore.gitHubProject?.branches || []
);
const importBranch = computed({
  get: () => integrationsStore.gitHubConfig.branch,
  set: (branch) => (integrationsStore.gitHubConfig.branch = branch),
});

const includePatterns = computed({
  get: () => integrationsStore.gitHubConfig.include || [],
  set: (include) => (integrationsStore.gitHubConfig.include = include),
});
const excludePatterns = computed({
  get: () => integrationsStore.gitHubConfig.exclude || [],
  set: (exclude) => (integrationsStore.gitHubConfig.exclude = exclude),
});
const artifactType = computed({
  get: () => integrationsStore.gitHubConfig.artifactType,
  set: (artifactType) =>
    (integrationsStore.gitHubConfig.artifactType = artifactType),
});

/**
 * Opens the documentation for file patterns.
 */
function handleFilePatternInfo() {
  window.open(
    "https://docs.oracle.com/en/java/javase/16/docs/api/java.base/java/nio/file/FileSystem.html#getPathMatcher(java.lang.String)"
  );
}

/**
 * Loads a user's GitHub projects for a selected organization.
 */
function handleReload() {
  if (!integrationsStore.gitHubOrganization) return;

  integrationsStore.gitHubProject = undefined;

  projects.value = gitHubApiStore.projectList.filter(
    ({ owner }) => owner === organizationName.value
  );
}

onMounted(() => handleReload());

watch(
  () => organizationName.value,
  () => handleReload()
);
</script>

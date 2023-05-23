<template>
  <stepper-list-step
    title="GitHub Repositories"
    empty-message="There are no repositories."
    :item-count="projects.length"
  >
    <list>
      <list-item
        v-for="item in projects"
        :key="item.name"
        :title="item.name"
        :subtitle="getRepositoryTime(item)"
        clickable
        :active="projectName === item.name"
        active-class="bg-background"
        @click="handleProjectSelect(item)"
      />
    </list>
    <flex-box v-if="!!projectName" column t="3">
      <select-input
        v-model="importBranch"
        label="Import Branch"
        :options="branches"
        hint="The branch to import files from."
      />
      <flex-box y="2" align="center">
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
      <text-input
        v-model="artifactType"
        label="Artifact Type"
        hint="The artifact type name to import these files as."
      />
    </flex-box>
  </stepper-list-step>
</template>

<script lang="ts">
/**
 * Allows for selecting a GitHub repository.
 */
export default {
  name: "GitHubProjectSelector",
};
</script>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from "vue";
import { GitHubProjectSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import {
  StepperListStep,
  List,
  ListItem,
  FlexBox,
  SelectInput,
  MultiselectInput,
} from "@/components/common";
import TextInput from "@/components/common/input/TextInput.vue";
import IconButton from "@/components/common/button/IconButton.vue";

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
  get: () => integrationsStore.gitHubConfig.include,
  set: (include) => (integrationsStore.gitHubConfig.include = include),
});
const excludePatterns = computed({
  get: () => integrationsStore.gitHubConfig.exclude,
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

  projects.value = integrationsStore.gitHubProjectList.filter(
    ({ owner }) => owner === organizationName.value
  );
}

/**
 * Returns a repository's last updated time.
 * @param repository - The repository to extract from.
 * @return The last updated time.
 */
function getRepositoryTime(repository: GitHubProjectSchema): string {
  const updated = new Date(repository.creationDate);

  return `Created on ${updated.getMonth()}/${updated.getDate()}/${updated.getFullYear()}`;
}

/**
 * SHandles a click to select a repository.
 * @param project - The repository to select.
 */
function handleProjectSelect(project: GitHubProjectSchema | undefined) {
  integrationsStore.selectGitHubProject(project);
}

onMounted(() => handleReload());

watch(
  () => organizationName.value,
  () => handleReload()
);
</script>

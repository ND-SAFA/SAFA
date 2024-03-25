<template>
  <div>
    <git-hub-authentication v-if="!integrationsStore.validGitHubCredentials" />
    <select-input
      v-else
      v-model="integrationsStore.gitHubOrganization"
      label="GitHub Organization"
      :options="gitHubApiStore.organizationList"
      :loading="gitHubApiStore.loading"
      hint="Required. You can also type in a public organization and click 'Enter'."
      class="full-width q-mb-sm"
      option-label="name"
      data-cy="input-github-organization"
      use-input
      clearable
      new-value-mode="add-unique"
      @new-value="
        (val) =>
          (integrationsStore.gitHubOrganization = {
            name: val || '',
            id: val || '',
          })
      "
    />
    <select-input
      v-if="!!integrationsStore.gitHubOrganization"
      v-model="integrationsStore.gitHubProject"
      label="GitHub Repository"
      :options="projects"
      hint="Required. You can also type in a public repository and click 'Enter'."
      class="full-width q-mb-sm"
      option-label="name"
      data-cy="input-github-project"
      use-input
      clearable
      new-value-mode="add-unique"
      @new-value="
        (val) =>
          (integrationsStore.gitHubProject = {
            name: val || '',
            id: val || '',
            description: '',
            size: 0,
            owner: integrationsStore.gitHubOrganization?.name || '',
            branches: [],
            defaultBranch: '',
            creationDate: '',
          })
      "
    />

    <flex-box v-if="!!projectName" column t="1">
      <select-input
        v-model="importBranch"
        label="Import Branch"
        :options="branches"
        class="full-width q-mb-sm"
        hint="The branch to import files from, using the default branch if not specified."
        use-input
        clearable
        new-value-mode="add-unique"
      />
      <multiselect-input
        v-model="filePaths"
        label="Import Path"
        :options="[]"
        add-values
        class="full-width q-mb-sm"
        hint="The file path(s) of the core code, such as 'src/'. Press enter to save."
      />
    </flex-box>

    <expansion-item
      v-if="!!integrationsStore.gitHubProject"
      label="Advanced Configuration"
    >
      <flex-box v-if="!!projectName" column t="1">
        <text-input
          v-if="!props.minimal"
          v-model="artifactType"
          label="Artifact Type"
          class="full-width q-mb-sm"
          hint="A name for imported artifacts."
        />

        <flex-box y="1" align="center">
          <div class="q-mr-sm">
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
            />
          </div>
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
import { GitHubProjectSchema, MinimalProps } from "@/types";
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

const props = defineProps<MinimalProps>();

const projects = ref<GitHubProjectSchema[]>([]);
const filePaths = ref<string[]>([]);

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

watch(
  () => integrationsStore.gitHubProject,
  () => {
    filePaths.value = [];
  }
);

watch(
  () => filePaths.value,
  (newPaths, oldPaths) => {
    const newGlobs = newPaths.map((path) =>
      path.endsWith("/") ? `${path}**` : `${path}/**`
    );
    const oldGlobs = oldPaths.map((path) =>
      path.endsWith("/") ? `${path}**` : `${path}/**`
    );

    const include = [
      ...(integrationsStore.gitHubConfig.include || []).filter(
        (pattern) => !oldGlobs.includes(pattern)
      ),
      ...newGlobs,
    ];

    // If the include array is empty, it will be removed from the config,
    // as an empty include means include no artifacts.
    if (include.length === 0) {
      integrationsStore.gitHubConfig.include = undefined;
    } else {
      integrationsStore.gitHubConfig.include = include;
    }
  }
);
</script>

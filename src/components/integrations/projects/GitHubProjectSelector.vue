<template>
  <generic-stepper-list-step
    title="GitHub Repositories"
    :item-count="repositories.length"
    :loading="repositoriesLoading"
    empty-message="There are no repositories."
  >
    <template slot="items">
      <template v-for="repository in repositories">
        <v-list-item
          three-line
          :key="repository.id"
          @click="handleRepositorySelect(repository)"
        >
          <v-list-item-icon v-if="!!repository.avatar_url">
            <v-avatar>
              <img :src="repository.avatar_url" :alt="repository.name" />
            </v-avatar>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="repository.name" />
            <v-list-item-subtitle v-text="getRepositorySubtitle(repository)" />
            <v-list-item-subtitle v-text="getRepositoryTime(repository)" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { GitHubProjectSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadGitHubProjects } from "@/api";
import { GenericStepperListStep } from "@/components/common";

/**
 * Allows for selecting a GitHub repository.
 */
export default Vue.extend({
  name: "GitHubProjectSelector",
  components: {
    GenericStepperListStep,
  },
  data() {
    return {
      repositories: [] as GitHubProjectSchema[],
      repositoriesLoading: false,
    };
  },
  mounted() {
    if (!integrationsStore.validGitHubCredentials) return;

    this.loadProjects();
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validGitHubCredentials;
    },
  },
  watch: {
    /**
     * Loads projects when credentials are valid.
     */
    hasCredentials(valid: boolean): void {
      if (!valid) return;

      this.loadProjects();
    },
  },
  methods: {
    /**
     * Loads a user's GitHub projects for a selected organization.
     */
    async loadProjects() {
      integrationsStore.gitHubProject = undefined;
      this.repositoriesLoading = true;

      handleLoadGitHubProjects({
        onSuccess: (repositories) => {
          this.repositories = repositories;
          this.repositoriesLoading = false;
        },
        onError: () => (this.repositoriesLoading = false),
      });
    },
    /**
     * Returns a repository's subtitle.
     * @param repository - The repository to extract from.
     * @return The subtitle.
     */
    getRepositorySubtitle(repository: GitHubProjectSchema): string {
      const { name, size } = repository;
      const subtitle = `${name} | ${size} File`;

      return size === 1 ? subtitle : `${subtitle}s`;
    },
    /**
     * Returns a repository's last updated time.
     * @param repository - The repository to extract from.
     * @return The last updated time.
     */
    getRepositoryTime(repository: GitHubProjectSchema): string {
      const updated = new Date(repository.created_at);

      return `Created on ${updated.getMonth()}/${updated.getDate()}/${updated.getFullYear()}`;
    },
    /**
     * SHandles a click to select a repository.
     * @param repository - The repository to select.
     */
    handleRepositorySelect(repository: GitHubProjectSchema | undefined) {
      integrationsStore.selectGitHubProject(repository);
    },
  },
});
</script>

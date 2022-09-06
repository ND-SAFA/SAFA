<template>
  <generic-stepper-list-step
    title="GitHub Repositories"
    :item-count="repositories.length"
    :loading="loading"
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
import Vue, { PropType } from "vue";
import { GitHubRepositoryModel } from "@/types";
import { GenericStepperListStep } from "@/components/common";

/**
 * Allows for selecting a GitHub repository.
 *
 * @emits `select` (GitHubRepository) - On repository selection.
 */
export default Vue.extend({
  name: "GitHubRepositorySelector",
  components: {
    GenericStepperListStep,
  },
  props: {
    repositories: {
      type: Array as PropType<GitHubRepositoryModel[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    /**
     * SHandles a click to select a repository.
     * @param repository - The repository to select.
     */
    handleRepositorySelect(repository: GitHubRepositoryModel) {
      this.$emit("select", repository);
    },
    /**
     * Returns a repository's subtitle.
     * @param repository - The repository to extract from.
     * @return The subtitle.
     */
    getRepositorySubtitle(repository: GitHubRepositoryModel): string {
      const { full_name, size } = repository;
      const subtitle = `${full_name} | ${size} File`;

      return size === 1 ? subtitle : `${subtitle}s`;
    },
    /**
     * Returns a repository's last updated time.
     * @param repository - The repository to extract from.
     * @return The last updated time.
     */
    getRepositoryTime(repository: GitHubRepositoryModel): string {
      const updated = new Date(repository.updated_at);

      return `Updated on ${updated.getMonth()}/${updated.getDate()}/${updated.getFullYear()}`;
    },
  },
});
</script>

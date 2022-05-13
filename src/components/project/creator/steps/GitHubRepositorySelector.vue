<template>
  <v-container>
    <h1 class="text-h5">GitHub Repositories</h1>
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <p v-else-if="repositories.length === 0" class="text-caption">
      There are no repositories.
    </p>
    <v-list>
      <v-list-item-group>
        <template v-for="repository in repositories">
          <v-list-item
            :key="repository.id"
            @click="handleRepositorySelect(repository)"
          >
            <v-list-item-icon>
              <v-avatar>
                <img :src="repository.avatar_url" :alt="repository.name" />
              </v-avatar>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="repository.name" />

              <v-list-item-subtitle
                v-text="getRepositorySubtitle(repository)"
              />
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GitHubRepository } from "@/types";

/**
 * Allows for selecting a GitHub repository.
 *
 * @emits `select` (GitHubRepository) - On repository selection.
 */
export default Vue.extend({
  name: "GitHubRepositorySelector",
  props: {
    repositories: {
      type: Array as PropType<GitHubRepository[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    handleRepositorySelect(repository: GitHubRepository) {
      this.$emit("select", repository);
    },
    getRepositorySubtitle(repository: GitHubRepository): string {
      const { full_name, size } = repository;
      const subtitle = `${full_name} | ${size} File`;

      return size === 1 ? subtitle : `${subtitle}s`;
    },
  },
});
</script>

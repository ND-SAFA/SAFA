<template>
  <v-container>
    <h1 class="text-h5">GitHub Installations</h1>
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <p v-else-if="installations.length === 0" class="text-caption">
      There are no installations.
    </p>
    <v-list>
      <v-list-item-group>
        <template v-for="installation in installations">
          <v-list-item
            :key="installation.id"
            @click="handleInstallationSelect(installation)"
          >
            <v-list-item-content>
              <v-list-item-title v-text="installation.name" />

              <v-list-item-subtitle v-text="installation.url" />
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GitHubInstallation } from "@/types";

/**
 * Allows for selecting a GitHub installation.
 *
 * @emits `select` (GitHubInstallation) - On site selection.
 */
export default Vue.extend({
  name: "GitHubInstallationSelector",
  props: {
    installations: {
      type: Array as PropType<GitHubInstallation[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    handleInstallationSelect(site: GitHubInstallation) {
      this.$emit("select", site);
    },
  },
});
</script>

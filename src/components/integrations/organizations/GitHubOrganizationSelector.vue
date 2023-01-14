<template>
  <stepper-list-step
    title="GitHub Organizations"
    :item-count="organizations.length"
    :loading="organizationsLoading"
    empty-message="There are no organizations."
  >
    <template slot="items">
      <template v-for="organization in organizations">
        <v-list-item
          three-line
          :key="organization.id"
          @click="handleOrganizationSelect(organization)"
        >
          <v-list-item-content>
            <v-list-item-title v-text="organization.name" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { GitHubOrganizationSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadGitHubOrganizations } from "@/api";
import { StepperListStep } from "@/components/common";

/**
 * Allows for selecting a GitHub organization.
 */
export default Vue.extend({
  name: "GitHubOrganizationSelector",
  components: {
    StepperListStep,
  },
  data() {
    return {
      organizations: [] as GitHubOrganizationSchema[],
      organizationsLoading: false,
    };
  },
  mounted() {
    this.loadOrganizations();
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
     * Loads organizations when credentials are valid.
     */
    hasCredentials(): void {
      this.loadOrganizations();
    },
  },
  methods: {
    /**
     * Loads a user's GitHub organizations.
     */
    async loadOrganizations() {
      if (!integrationsStore.validGitHubCredentials) return;

      integrationsStore.gitHubOrganization = undefined;
      this.organizationsLoading = true;

      handleLoadGitHubOrganizations({
        onSuccess: (organizations) => {
          this.organizations = organizations;
          this.organizationsLoading = false;
        },
        onError: () => (this.organizationsLoading = false),
      });
    },
    /**
     * Handles a click to select an organization.
     * @param organization - The organization to select.
     */
    handleOrganizationSelect(
      organization: GitHubOrganizationSchema | undefined
    ) {
      integrationsStore.selectGitHubOrganization(organization);
    },
  },
});
</script>

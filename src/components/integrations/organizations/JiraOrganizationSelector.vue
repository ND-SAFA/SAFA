<template>
  <stepper-list-step
    title="Jira Organizations"
    empty-message="There are no organizations."
    :item-count="organizations.length"
    :loading="organizationsLoading"
  >
    <template v-for="organization in organizations">
      <v-list-item
        :key="organization.id"
        @click="handleOrganizationSelect(organization)"
      >
        <v-list-item-content>
          <v-list-item-title v-text="organization.name" />
        </v-list-item-content>
      </v-list-item>
    </template>
  </stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraOrganizationSchema } from "@/types";
import { integrationsStore } from "@/hooks";
import { handleLoadJiraOrganizations } from "@/api";
import { StepperListStep } from "@/components";

/**
 * Allows for selecting a jira organization.
 */
export default Vue.extend({
  name: "JiraOrganizationSelector",
  components: {
    StepperListStep,
  },
  data() {
    return {
      organizations: [] as JiraOrganizationSchema[],
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
      return integrationsStore.validJiraCredentials;
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
     * Loads a user's Jira organizations.
     */
    async loadOrganizations() {
      if (!integrationsStore.validJiraCredentials) return;

      integrationsStore.jiraOrganization = undefined;
      this.organizationsLoading = true;

      handleLoadJiraOrganizations({
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
    handleOrganizationSelect(organization: JiraOrganizationSchema | undefined) {
      integrationsStore.selectJiraOrganization(organization);
    },
  },
});
</script>

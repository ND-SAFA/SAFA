import { defineStore } from "pinia";

import {
  GitHubOrganizationSchema,
  GitHubProjectSchema,
  JiraOrganizationSchema,
  JiraProjectSchema,
} from "@/types";
import { pinia } from "@/plugins";

/**
 * This module defines the state of 3rd party integrations.
 */
export const useIntegrations = defineStore("integrations", {
  state: () => ({
    /**
     * Whether this user is connected to Jira.
     */
    validJiraCredentials: false,
    /**
     * A selected Jira installation to import from.
     */
    jiraOrganization: undefined as JiraOrganizationSchema | undefined,
    /**
     * A selected Jira project to import.
     */
    jiraProject: undefined as JiraProjectSchema | undefined,
    /**
     * Whether this user is connected to GitHub.
     */
    validGitHubCredentials: false,
    /**
     * A selected GitHub installation to import from.
     */
    gitHubOrganization: undefined as GitHubOrganizationSchema | undefined,
    /**
     * A selected GitHub project to import.
     */
    gitHubProject: undefined as GitHubProjectSchema | undefined,
  }),
  getters: {},
  actions: {
    /**
     * Selects a Jira organization.
     *
     * @param organization - The organization to select.
     */
    selectJiraOrganization(
      organization: JiraOrganizationSchema | undefined
    ): void {
      if (
        !this.jiraOrganization ||
        this.jiraOrganization?.id !== organization?.id
      ) {
        this.jiraOrganization = organization;
      } else {
        this.jiraOrganization = undefined;
      }
    },
    /**
     * Selects a Jira project.
     *
     * @param project - The project to select.
     */
    selectJiraProject(project: JiraProjectSchema | undefined): void {
      if (!this.jiraProject || this.jiraProject?.id !== project?.id) {
        this.jiraProject = project;
      } else {
        this.jiraProject = undefined;
      }
    },
    /**
     * Selects a GitHub organization.
     *
     * @param organization - The organization to select.
     */
    selectGitHubOrganization(
      organization: GitHubOrganizationSchema | undefined
    ): void {
      if (
        !this.gitHubOrganization ||
        this.gitHubOrganization?.id !== organization?.id
      ) {
        this.gitHubOrganization = organization;
      } else {
        this.gitHubOrganization = undefined;
      }
    },
    /**
     * Selects a GitHub project.
     *
     * @param project - The project to select.
     */
    selectGitHubProject(project: GitHubProjectSchema | undefined): void {
      if (!this.gitHubProject || this.gitHubProject?.id !== project?.id) {
        this.gitHubProject = project;
      } else {
        this.gitHubProject = undefined;
      }
    },
  },
});

export default useIntegrations(pinia);

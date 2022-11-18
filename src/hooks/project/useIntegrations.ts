import { defineStore } from "pinia";

import { GitHubProjectModel, JiraProjectModel } from "@/types";
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
     * A selected Jira project to import.
     */
    jiraProject: undefined as JiraProjectModel | undefined,
    /**
     * Whether this user is connected to GitHub.
     */
    validGitHubCredentials: false,
    /**
     * A selected GitHub project to import.
     */
    gitHubProject: undefined as GitHubProjectModel | undefined,
  }),
  getters: {},
  actions: {
    /**
     * Selects a Jira project.
     *
     * @param project - The project to select.
     */
    selectJiraProject(project: JiraProjectModel | undefined): void {
      if (!this.jiraProject || this.jiraProject?.id !== project?.id) {
        this.jiraProject = project;
      } else {
        this.jiraProject = undefined;
      }
    },
    /**
     * Selects a GitHub project.
     *
     * @param project - The project to select.
     */
    selectGitHubProject(project: GitHubProjectModel | undefined): void {
      if (!this.gitHubProject || this.gitHubProject?.id !== project?.id) {
        this.gitHubProject = project;
      } else {
        this.gitHubProject = undefined;
      }
    },
  },
});

export default useIntegrations(pinia);

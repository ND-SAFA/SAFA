import { ComputedRef, Ref } from "vue";
import {
  GitHubOrganizationSchema,
  GitHubProjectSchema,
  IOHandlerCallback,
} from "@/types";

/**
 * A hook for calling GitHub API endpoints.
 */
export interface GitHubApiHook {
  /**
   * The list of GitHub organizations for the current user.
   */
  organizationList: Ref<GitHubOrganizationSchema[]>;
  /**
   * The list of GitHub projects for the current user and selected organization.
   */
  projectList: Ref<GitHubProjectSchema[]>;
  /**
   * Whether a GitHub request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Opens the GitHub authentication window.
   */
  handleAuthRedirect(): void;
  /**
   * Clears the saved GitHub credentials.
   */
  handleDeleteCredentials(): Promise<void>;
  /**
   * Handles GitHub authentication when the app loads.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleVerifyCredentials(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Loads GitHub projects and creates related organizations.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleLoadProjects(
    callbacks?: IOHandlerCallback<GitHubProjectSchema[]>
  ): Promise<void>;
}

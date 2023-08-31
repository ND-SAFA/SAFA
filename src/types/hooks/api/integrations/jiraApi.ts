import { ComputedRef, Ref } from "vue";
import {
  IOHandlerCallback,
  JiraOrganizationSchema,
  JiraProjectSchema,
} from "@/types";

/**
 * A hook for calling Jira API endpoints.
 */
export interface JiraApiHook {
  /**
   * The list of jira organizations for the current user.
   */
  organizationList: Ref<JiraOrganizationSchema[]>;
  /**
   * The list of jira projects for the current user and selected organization.
   */
  projectList: Ref<JiraProjectSchema[]>;
  /**
   * Whether a jira request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Opens the Jira authentication window.
   */
  handleAuthRedirect(): void;
  /**
   * Clears the saved Jira credentials.
   */
  handleDeleteCredentials(): Promise<void>;
  /**
   * Handles Jira authentication when the app loads.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleVerifyCredentials(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Loads Jira installations.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleLoadOrganizations(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Loads Jira projects and sets the currently selected cloud id.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleLoadProjects(callbacks?: IOHandlerCallback): Promise<void>;
}

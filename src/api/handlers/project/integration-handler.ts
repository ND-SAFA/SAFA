import {
  GitHubProjectSchema,
  InstallationSchema,
  IOHandlerCallback,
  JiraOrganizationSchema,
  JiraProjectSchema,
} from "@/types";
import { integrationsStore, logStore, projectStore } from "@/hooks";
import { getParam, QueryParams } from "@/router";
import {
  getGitHubCredentials,
  getGitHubProjects,
  getJiraCredentials,
  getJiraProjects,
  refreshGitHubCredentials,
  refreshJiraCredentials,
  saveGitHubCredentials,
  saveJiraCredentials,
  getProjectInstallations,
  createGitHubProjectSync,
  createJiraProjectSync,
  handleJobSubmission,
  getJiraInstallations,
} from "@/api";

/**
 * Handles loading installations affiliated with the current project.
 *
 * @param onComplete - Called once the action is complete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleLoadInstallations({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): void {
  getProjectInstallations(projectStore.projectId)
    .then((installations) => {
      integrationsStore.installations = installations;
      onSuccess?.();
    })
    .catch(onError)
    .finally(onComplete);
}

/**
 * Syncs the current project with the selected installation's data.
 *
 * @param installation - The installation to sync data with.
 * @param onComplete - Called once the action is complete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export async function handleSyncInstallation(
  installation: Omit<InstallationSchema, "lastUpdate">,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  try {
    if (installation.type === "GITHUB") {
      const job = await createGitHubProjectSync(
        projectStore.versionId,
        installation.installationId
      );

      await handleJobSubmission(job);
    } else if (installation.type === "JIRA") {
      const job = await createJiraProjectSync(
        projectStore.versionId,
        installation.installationOrgId,
        installation.installationId
      );

      await handleJobSubmission(job);
    } else {
      throw new Error("Unknown installation type");
    }

    logStore.onSuccess(
      `Integration data is being synced: ${installation.installationId}. 
       You'll receive a notification once data has completed syncing.`
    );
    onSuccess?.();
  } catch (e) {
    logStore.onError(`Unable to sync integration data: ${e}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Handles Jira authentication when the app loads.
 *
 * @param onComplete - Called when the action completes.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeJira({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): void {
  const accessCode =
    getParam(QueryParams.TAB) === "jira"
      ? getParam(QueryParams.JIRA_TOKEN)
      : "";

  const handleSuccess = () => {
    integrationsStore.validJiraCredentials = true;
    onSuccess?.();
  };
  const handleError = (e: Error) => {
    integrationsStore.validJiraCredentials = false;
    onError?.(e);
  };

  if (accessCode) {
    saveJiraCredentials(String(accessCode))
      .then(handleSuccess)
      .catch((e) => {
        logStore.onError("Unable to read Jira access code.");
        handleError(e);
      })
      .finally(onComplete);
  } else {
    getJiraCredentials()
      .then(async (valid) => {
        if (valid) return;

        const refreshValid = await refreshJiraCredentials();

        if (!refreshValid) {
          throw new Error("Invalid refresh");
        }
      })
      .then(handleSuccess)
      .catch(handleError)
      .finally(onComplete);
  }
}

/**
 * Loads Jira installations.
 *
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraOrganizations({
  onSuccess,
  onError,
}: IOHandlerCallback<JiraOrganizationSchema[]>): void {
  getJiraInstallations()
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}

/**
 * Loads Jira projects and sets the currently selected cloud id.
 *
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadJiraProjects({
  onSuccess,
  onError,
}: IOHandlerCallback<JiraProjectSchema[]>): void {
  const installationId = integrationsStore.jiraOrganization?.id;

  if (!installationId) return;

  getJiraProjects(installationId)
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}

/**
 * Handles GitHub authentication when the app loads.
 *
 * @param onComplete - Called when the action completes.
 * @param onSuccess - Called if the action is successful, with the GitHub authorization token.
 * @param onError - Called if the action fails.
 */
export function handleAuthorizeGitHub({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): void {
  const accessCode =
    getParam(QueryParams.TAB) === "github"
      ? getParam(QueryParams.GITHUB_TOKEN)
      : "";

  const handleSuccess = () => {
    integrationsStore.validGitHubCredentials = true;
    onSuccess?.();
  };
  const handleError = (e: Error) => {
    integrationsStore.validGitHubCredentials = false;
    onError?.(e);
  };

  if (accessCode) {
    saveGitHubCredentials(String(accessCode))
      .then(handleSuccess)
      .catch((e) => {
        logStore.onError("Unable to read GitHub access code.");
        handleError(e);
      })
      .finally(onComplete);
  } else {
    getGitHubCredentials()
      .then(async (valid) => {
        if (valid) return;

        const refreshValid = await refreshGitHubCredentials();

        if (!refreshValid) {
          throw new Error("Invalid refresh");
        }
      })
      .then(handleSuccess)
      .catch(handleError)
      .finally(onComplete);
  }
}

/**
 * Loads GitHub projects and sets the currently selected cloud id.
 *
 * @param onSuccess - Called if the action is successful, with the jira project list.
 * @param onError - Called if the action fails.
 */
export function handleLoadGitHubProjects({
  onSuccess,
  onError,
}: IOHandlerCallback<GitHubProjectSchema[]>): void {
  getGitHubProjects()
    .then(onSuccess)
    .catch((e) => {
      onError?.(e);
      logStore.onError(e);
    });
}

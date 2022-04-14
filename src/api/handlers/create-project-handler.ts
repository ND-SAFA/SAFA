import { appModule, logModule } from "@/store";
import { postJiraProject, saveOrUpdateProject, setCreatedProject } from "@/api";
import { Project } from "@/types";
import { navigateTo, Routes } from "@/router";

/**
 * Creates a new project, and sets related app state.
 *
 * @param project - The project to create.
 * @throws If project creation fails.
 */
export async function handleImportProject(project: Project): Promise<void> {
  appModule.onLoadStart();

  try {
    const res = await saveOrUpdateProject(project);

    await navigateTo(Routes.ARTIFACT);
    await setCreatedProject(res);
  } catch (e) {
    logModule.onError("Unable to import project");
    throw e;
  } finally {
    appModule.onLoadEnd();
  }
}

/**
 * Creates a new project based on a Jira project, and sets related app state.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @param cloudId - The Jira cloud id for the current company.
 * @param projectId - The Jira project id to import.
 * @throws If project creation fails.
 */
export async function handleImportJiraProject(
  accessToken: string,
  cloudId: string,
  projectId: string
): Promise<void> {
  appModule.onLoadStart();

  try {
    await postJiraProject(accessToken, cloudId, projectId);
  } catch (e) {
    logModule.onError("Unable to import jira project");
    throw e;
  } finally {
    appModule.onLoadEnd();
  }
}

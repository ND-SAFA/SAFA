import { navigateTo, Routes } from "@/router";
import { sessionModule } from "@/store";
import {
  getCurrentVersion,
  getProjects,
  loadVersionIfExistsHandler,
} from "@/api";

/**
 * Loads the last stored project.
 */
export async function loadLastProject(): Promise<void> {
  const projects = await getProjects();

  if (projects.length) {
    const versionId = (await getCurrentVersion(projects[0].projectId))
      .versionId;

    await sessionModule.updateSession({ versionId });
    await loadVersionIfExistsHandler(versionId).catch(() =>
      navigateTo(Routes.PROJECT_CREATOR)
    );
  } else {
    await navigateTo(Routes.PROJECT_CREATOR);
  }
}

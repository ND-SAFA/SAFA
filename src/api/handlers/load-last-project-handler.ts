import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { sessionModule } from "@/store";
import { getCurrentVersion, getProjects, handleLoadVersion } from "@/api";

/**
 * Loads the last stored project.
 */
export async function handleLoadLastProject(): Promise<void> {
  let versionId = getParam(QueryParams.VERSION);

  if (!versionId) {
    const projects = await getProjects();

    if (projects.length > 0) {
      versionId = (await getCurrentVersion(projects[0].projectId)).versionId;
    }
  }
  if (versionId && typeof versionId === "string") {
    await sessionModule.updateSession({ versionId });
    await handleLoadVersion(versionId).catch(() =>
      navigateTo(Routes.PROJECT_CREATOR)
    );
  } else {
    await navigateTo(Routes.PROJECT_CREATOR);
  }
}

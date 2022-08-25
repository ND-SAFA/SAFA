import { sessionStore, logStore } from "@/hooks";
import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { getCurrentVersion, getProjects, handleLoadVersion } from "@/api";

/**
 * Loads the last stored project.
 */
export async function handleLoadLastProject(): Promise<void> {
  if (!sessionStore.doesSessionExist) return;

  let versionId = getParam(QueryParams.VERSION);

  if (!versionId) {
    const projects = await getProjects();

    if (projects.length > 0) {
      versionId = (await getCurrentVersion(projects[0].projectId)).versionId;
    }
  }
  if (typeof versionId === "string") {
    await handleLoadVersion(versionId).catch((e) => {
      logStore.onDevInfo(e);
      navigateTo(Routes.HOME);
    });
  } else {
    await navigateTo(Routes.HOME);
  }
}

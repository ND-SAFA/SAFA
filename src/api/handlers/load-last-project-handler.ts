import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { getCurrentVersion, getProjects, handleLoadVersion } from "@/api";
import { URLParameter } from "@/types";
import { logModule } from "@/store";

/**
 * Loads a version, if it exists.
 */
export async function handleLoadVersionIfExists(
  versionId?: URLParameter
): Promise<void> {
  if (typeof versionId === "string") {
    await handleLoadVersion(versionId).catch((e) => {
      logModule.onDevError(e);
      navigateTo(Routes.HOME);
    });
  } else {
    await navigateTo(Routes.HOME);
  }
}

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
  await handleLoadVersionIfExists(versionId);
}

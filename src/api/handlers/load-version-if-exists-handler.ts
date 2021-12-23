import { appModule, projectModule } from "@/store";
import { getProjectVersion } from "@/api";
import { navigateTo, Routes } from "@/router";

/**
 * Load the given project version of given Id. Navigates to the artifact
 * tree page in order to show the new project.
 *
 * @param lastVersionId The id of the version to retrieve and load.
 */
export async function loadVersionIfExistsHandler(
  lastVersionId: string | undefined
): Promise<void> {
  if (lastVersionId) {
    appModule.onLoadStart();

    return navigateTo(Routes.ARTIFACT_TREE)
      .then(() => getProjectVersion(lastVersionId))
      .then(projectModule.setProjectCreationResponse)
      .finally(appModule.onLoadEnd);
  }
}

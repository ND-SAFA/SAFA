import { EmptyLambda, ProjectCreationResponse } from "@/types";
import { logModule, viewportModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import {
  connectAndSubscribeToVersion,
  updateProjectThroughFlatFiles,
} from "@/api/endpoints";
import { setCreatedProject } from "@/api";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 *
 * @param projectId - The project that has been selected by the user
 * @param versionId - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful
 * @param onLoadStart - Callback to indicate that loading should be displayed
 * @param onLoadEnd - Callback to indicate that loading has finished
 * @param onFinally - Callback to call if upload was successful.
 */
export async function uploadNewProjectVersion(
  projectId: string,
  versionId: string,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean,
  onLoadStart: EmptyLambda,
  onLoadEnd: EmptyLambda,
  onFinally: EmptyLambda
): Promise<void> {
  if (selectedFiles.length === 0) {
    logModule.onWarning("Please at least one file to upload");
  } else {
    onLoadStart();
    const formData = new FormData();
    selectedFiles.forEach((file: File) => {
      formData.append("files", file);
    });
    if (setVersionIfSuccessful) {
      connectAndSubscribeToVersion(projectId, versionId).catch((e) =>
        logModule.onError(e.message)
      );
    }

    updateProjectThroughFlatFiles(versionId, formData)
      .then(async (res: ProjectCreationResponse) => {
        logModule.onSuccess(
          `Flat files were uploaded successfully and ${res.project.name} was updated.`
        );
        if (setVersionIfSuccessful) {
          await navigateTo(Routes.ARTIFACT_TREE);
          await setCreatedProject(res);
          await viewportModule.setArtifactTreeLayout();
        }
      })
      .finally(() => {
        onLoadEnd();
        onFinally();
      });
  }
}

import {
  EmptyLambda,
  ProjectIdentifier,
  ProjectVersion,
  ProjectCreationResponse,
} from "@/types";
import { logModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import {
  connectAndSubscribeToVersion,
  updateProjectThroughFlatFiles,
} from "@/api/endpoints";
import { setAndSubscribeToProject, setCreatedProject } from "@/api";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 *
 * @param selectedProject - The project that has been selected by the user
 * @param selectedVersion - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful
 * @param onLoadStart - Callback to indicate that loading should be displayed
 * @param onLoadEnd - Callback to indicate that loading has finished
 * @param onFinally - Callback to call if upload was successful.
 */
export async function uploadNewProjectVersion(
  selectedProject: ProjectIdentifier | undefined,
  selectedVersion: ProjectVersion | undefined,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean,
  onLoadStart: EmptyLambda,
  onLoadEnd: EmptyLambda,
  onFinally: EmptyLambda
): Promise<void> {
  if (selectedProject === undefined) {
    logModule.onWarning("Please select a project to update");
  } else if (selectedVersion === undefined) {
    logModule.onWarning("Please select a version to upload to");
  } else if (selectedFiles.length === 0) {
    logModule.onWarning("Please at least one file to upload");
  } else {
    onLoadStart();
    const formData = new FormData();
    selectedFiles.forEach((file: File) => {
      formData.append("files", file);
    });
    if (setVersionIfSuccessful) {
      connectAndSubscribeToVersion(
        selectedProject.projectId,
        selectedVersion.versionId
      ).catch((e) => logModule.onError(e.message));
    }

    updateProjectThroughFlatFiles(selectedVersion.versionId, formData)
      .then(async (res: ProjectCreationResponse) => {
        logModule.onSuccess(
          `Flat files were uploaded successfully and ${res.project.name} was updated.`
        );
        if (setVersionIfSuccessful) {
          await navigateTo(Routes.ARTIFACT_TREE);
          await setCreatedProject(res);
        }
      })
      .finally(() => {
        onLoadEnd();
        onFinally();
      });
  }
}

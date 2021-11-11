import { ProjectIdentifier, ProjectVersion } from "@/types";
import { appModule, projectModule } from "@/store";
import { updateProjectThroughFlatFiles } from "@/api/project-api";
import { ProjectCreationResponse } from "@/types";
import { navigateTo, Routes } from "@/router";

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
  onLoadStart: () => void,
  onLoadEnd: () => void,
  onFinally: () => void
): Promise<void> {
  if (selectedProject === undefined) {
    appModule.onWarning("Please select a project to update");
  } else if (selectedVersion === undefined) {
    appModule.onWarning("Please select a version to upload to");
  } else if (selectedFiles.length === 0) {
    appModule.onWarning("Please at least one file to upload");
  } else {
    onLoadStart();
    const formData = new FormData();
    selectedFiles.forEach((file: File) => {
      formData.append("files", file);
    });
    if (setVersionIfSuccessful) {
      await projectModule
        .subscribeToVersion({
          projectId: selectedProject.projectId,
          versionId: selectedVersion.versionId,
        })
        .catch((e) => appModule.onError(e.message));
    }

    updateProjectThroughFlatFiles(selectedVersion.versionId, formData)
      .then(async (res: ProjectCreationResponse) => {
        appModule.onSuccess(
          `Flat files were uploaded successfully and ${res.project.name} was updated.`
        );
        if (setVersionIfSuccessful) {
          await navigateTo(Routes.ARTIFACT_TREE);
        }
      })
      .finally(() => {
        onLoadEnd();
        onFinally();
      });
  }
}

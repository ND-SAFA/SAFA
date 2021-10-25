import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import { appModule, projectModule } from "@/store";
import { updateProjectThroughFlatFiles } from "@/api/project-api";
import { ProjectCreationResponse } from "@/types/api";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 * @param selectedProject - The project that has been selected by the user
 * @param selectedVersion - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful
 * @param onLoadStart - Callback to indicate that loading should be displayed
 * @param onLoadEnd - Callback to indicate that loading has finsihed
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
      .then((res: ProjectCreationResponse) => {
        appModule.onSuccess(
          `Flat files were uploaded successfuly and ${res.project.name} was updated.`
        );
      })
      .finally(() => {
        onLoadEnd();
        onFinally();
      });
  }
}

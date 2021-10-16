import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import store, { appModule, projectModule } from "@/store";
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
 * @param onSuccess - Callback to call if upload was successful.
 */
export function uploadNewProjectVersion(
  selectedProject: ProjectIdentifier | undefined,
  selectedVersion: ProjectVersion | undefined,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean,
  onLoadStart: () => void,
  onLoadEnd: () => void,
  onSuccess: () => void
): void {
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
      projectModule.subscribeToVersion({
        projectId: selectedProject.projectId,
        versionId: selectedVersion.versionId,
      });
    }

    updateProjectThroughFlatFiles(selectedVersion.versionId, formData)
      .then((res: ProjectCreationResponse) => {
        onLoadEnd();
        appModule.onSuccess(
          `Flat files were uploaded successfuly and ${res.project.name} was updated.`
        );

        onSuccess();
      })
      .catch((e) => {
        onLoadEnd();
        appModule.onError(e.message);
      });
  }
}

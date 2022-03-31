import { logModule } from "@/store";
import { navigateTo, QueryParams, Routes } from "@/router";
import {
  connectAndSubscribeToVersion,
  updateProjectThroughFlatFiles,
} from "@/api/endpoints";
import { setCreatedProject } from "@/api";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 *
 * @param projectId - The project that has been selected by the user.
 * @param versionId - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version.
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful.
 */
export async function uploadNewProjectVersion(
  projectId: string,
  versionId: string,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean
): Promise<void> {
  if (selectedFiles.length === 0) {
    logModule.onWarning("Please add at least one file to upload");
  } else {
    const formData = new FormData();

    selectedFiles.forEach((file: File) => {
      formData.append("files", file);
    });

    if (setVersionIfSuccessful) {
      connectAndSubscribeToVersion(projectId, versionId).catch((e) =>
        logModule.onError(e.message)
      );
    }

    const res = await updateProjectThroughFlatFiles(versionId, formData);

    logModule.onSuccess(
      `Flat files were uploaded successfully and ${res.project.name} was updated.`
    );

    if (setVersionIfSuccessful) {
      await navigateTo(Routes.ARTIFACT, { [QueryParams.VERSION]: versionId });
      await setCreatedProject(res);
    }
  }
}

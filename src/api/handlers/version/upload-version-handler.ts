import { appModule, logModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { handleSelectVersion } from "@/api/notifications";
import { handleJobSubmission } from "@/api/handlers/project/job-handler";
import { createFlatFileUploadJob } from "@/api";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 *
 * @param projectId - The project that has been selected by the user.
 * @param versionId - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version.
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful.
 * @param isCompleteSet - Whether to delete any other artifacts in the current version.
 */
export async function handleUploadProjectVersion(
  projectId: string,
  versionId: string,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean,
  isCompleteSet = false
): Promise<void> {
  if (selectedFiles.length === 0) {
    logModule.onWarning("Please add at least one file to upload.");
  } else {
    const formData = new FormData();

    selectedFiles.forEach((file: File) => {
      formData.append("files", file);
    });

    formData.append("isCompleteSet", JSON.stringify(isCompleteSet));

    if (setVersionIfSuccessful) {
      handleSelectVersion(projectId, versionId).catch((e) =>
        logModule.onError(e.message)
      );
    }

    const uploadFlatFiles = async () => {
      const job = await createFlatFileUploadJob(versionId, formData);
      await handleJobSubmission(job);
      logModule.onSuccess(`Project upload has been submitted.`);
      return job;
    };

    if (setVersionIfSuccessful) {
      try {
        appModule.onLoadStart();
        await handleSelectVersion(projectId, versionId);
        await uploadFlatFiles();
      } catch (e) {
        logModule.onError(e.message);
      } finally {
        await navigateTo(Routes.UPLOAD_STATUS);
        appModule.onLoadEnd();
      }
    } else {
      await uploadFlatFiles();
    }
  }
}

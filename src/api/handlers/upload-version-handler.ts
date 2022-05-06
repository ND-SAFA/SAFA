import { appModule, logModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { updateProjectThroughFlatFiles } from "@/api";
import { connectAndSubscribeToVersion } from "@/api/notifications";
import { handleJobSubmission } from "@/api/handlers/job-handler";

/**
 * Responsible for validating and uploading the flat files to a project at a specified version.
 *
 * @param projectId - The project that has been selected by the user.
 * @param versionId - The version associated with given project to update.
 * @param selectedFiles  - The flat files that will update given version.
 * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful.
 */
export async function handleUploadProjectVersion(
  projectId: string,
  versionId: string,
  selectedFiles: File[],
  setVersionIfSuccessful: boolean
): Promise<void> {
  if (selectedFiles.length === 0) {
    logModule.onWarning("Please add at least one file to upload.");
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

    const uploadFlatFiles = async () => {
      const res = await updateProjectThroughFlatFiles(versionId, formData);

      logModule.onSuccess(`Job has been successfully submitted.`);

      return res;
    };

    if (setVersionIfSuccessful) {
      try {
        appModule.onLoadStart();
        connectAndSubscribeToVersion(projectId, versionId).catch((e) =>
          logModule.onError(e.message)
        );
        // Note that changing the order below will cause the project to not properly render initially.
        await navigateTo(Routes.ARTIFACT);
        const job = await uploadFlatFiles();
        await handleJobSubmission(job);
      } catch (e) {
        logModule.onError(e.message);
        await navigateTo(Routes.UPLOAD_STATUS);
      } finally {
        appModule.onLoadEnd();
      }
    } else {
      await uploadFlatFiles();
    }
  }
}

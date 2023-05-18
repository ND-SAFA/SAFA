import { saveAs } from "file-saver";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { getProjectFiles } from "@/api";

/**
 * Creates a file download for project files, either in csv for json format.
 * @param fileType - The file format to download.
 */
export async function handleDownloadProject(
  fileType: "csv" | "json" = "csv"
): Promise<void> {
  const data = await getProjectFiles(projectStore.versionId, fileType);

  const fileName = `${projectStore.project.name}-${versionToString(
    projectStore.version
  )}.zip`;
  const blob = new Blob([data], {
    type: "application/octet-stream",
  });

  saveAs(blob, fileName);
}

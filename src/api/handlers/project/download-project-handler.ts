import { saveAs } from "file-saver";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { getProjectFiles } from "@/api";

/**
 * Creates a file download for project csv files.
 */
export async function handleDownloadProjectCSV(): Promise<void> {
  const data = await getProjectFiles(projectStore.versionId);

  const fileName = `${projectStore.project.name}-${versionToString(
    projectStore.version
  )}.zip`;
  const blob = new Blob([data], {
    type: "application/octet-stream",
  });

  saveAs(blob, fileName);
}

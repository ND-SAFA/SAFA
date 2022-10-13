import { saveAs } from "file-saver";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { getProjectFiles } from "@/api";

/**
 * Creates a file download for project csv files.
 */
export async function handleDownloadProjectCSV(): Promise<void> {
  const data = await getProjectFiles(projectStore.versionId);

  console.log(data);

  const blob = new Blob([data], {
    type: "text/csv;charset=utf-8",
  });

  saveAs(
    blob,
    `${projectStore.project.name}-${versionToString(projectStore.version)}.csv`
  );
}

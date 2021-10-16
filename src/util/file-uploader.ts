import os from "os";
import { remote } from "electron";
import { readFileBase64 } from "@/util/os-helper";

export interface UploadFilesResponse {
  [key: string]: string;
}

export async function uploadFiles(
  files: string[]
): Promise<UploadFilesResponse> {
  const results = await Promise.all(
    files.map(async (file) => {
      const myData: string = await readFileBase64(file);
      let pieces = [];
      if (os.platform() === "win32") {
        pieces = file.split("\\");
      } else {
        pieces = file.split("/");
      }
      return [pieces[pieces.length - 1], myData];
    })
  );
  const dict: UploadFilesResponse = {};
  for (const result of results) {
    const r0: string = result[0];
    dict[r0] = result[1];
  }
  return dict;
}

export async function getMultiSelectFiles(): Promise<string[]> {
  return new Promise((resolve, reject) => {
    const { dialog } = remote;
    dialog
      .showOpenDialog({
        properties: ["openFile", "multiSelections"],
      })
      .then((chosenFolders) => {
        if (!chosenFolders.canceled) {
          resolve(chosenFolders.filePaths);
        } else {
          resolve([]);
        }
      })
      .catch(reject);
  });
}

export async function readFiles(
  filePaths: string[]
): Promise<Record<string, string>> {
  const results: string[][] = await Promise.all(
    filePaths.map(async (file) => {
      const myData = await readFileBase64(file);
      let pieces = [];
      if (os.platform() === "win32") {
        pieces = file.split("\\");
      } else {
        pieces = file.split("/");
      }
      const fileName: string = pieces[pieces.length - 1];
      return [fileName, myData];
    })
  );
  const dict: Record<string, string> = {};
  for (const result of results) {
    dict[result[0]] = result[1];
  }
  return dict;
}

export async function createFormData(
  filesData: Record<string, string>
): Promise<FormData> {
  const formData = new FormData();
  for (const [fileName, fileContent] of Object.entries(filesData)) {
    formData.append("files", new Blob([fileContent]), fileName);
  }
  return formData;
}

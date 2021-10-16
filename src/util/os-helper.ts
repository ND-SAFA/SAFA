import fs from "fs/promises";

export function readFileBase64(fileName: string): Promise<string> {
  return fs.readFile(fileName, {
    encoding: "base64",
  });
}

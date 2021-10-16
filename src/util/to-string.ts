import { ProjectVersion } from "@/types/domain/project";

export function versionToString(
  currentVersion: ProjectVersion | undefined
): string {
  if (currentVersion === undefined) {
    return "X.X.X";
  }
  return `${currentVersion.majorVersion}.${currentVersion.minorVersion}.${currentVersion.revision}`;
}

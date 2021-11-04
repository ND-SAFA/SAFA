import { ProjectVersion } from "@/types/domain/project";

/**
 * Stringifies the version number.
 *
 * @param currentVersion - The current version number.
 *
 * @return The stringified version number.
 */
export function versionToString(currentVersion?: ProjectVersion): string {
  if (currentVersion === undefined) {
    return "X.X.X";
  }
  return `${currentVersion.majorVersion}.${currentVersion.minorVersion}.${currentVersion.revision}`;
}

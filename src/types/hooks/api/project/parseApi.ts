import { ArtifactMap, CreatorFilePanel } from "@/types";

/**
 * A hook for calling file parsing API endpoints.
 */
export interface ParseApiHook {
  /**
   * Parses a file for the project creator.
   *
   * @param panel - The panel to parse the file of.
   * @param artifactMap - A collection of all parsed artifacts, keyed by name.
   */
  handleParseProjectFile(
    panel: CreatorFilePanel,
    artifactMap: ArtifactMap
  ): Promise<void>;
}

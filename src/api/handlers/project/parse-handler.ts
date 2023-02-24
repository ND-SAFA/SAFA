import { CreatorFilePanel } from "@/types";
import { parseArtifactFile } from "@/api";

/**
 * Parses a file for the project creator.
 *
 * @param panel - The panel to parse the file of.
 */
export function parseFilePanel(panel: CreatorFilePanel): void {
  if (!panel.file) return;

  if (panel.variant === "artifact") {
    parseArtifactFile(panel.type, panel.file)
      .then(({ entities, errors }) => {
        panel.artifacts = entities;
        panel.errorMessage =
          errors.length === 0 ? undefined : errors.join(", ");
      })
      .catch(() => {
        panel.errorMessage = "Unable to parse this file";
      });
  }
}

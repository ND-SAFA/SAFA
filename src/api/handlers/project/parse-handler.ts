import { ArtifactMap, CreatorFilePanel, TraceLinkSchema } from "@/types";
import { extractTraceId } from "@/util";
import { parseArtifactFile, parseTraceFile } from "@/api";

/**
 * Parses a file for the project creator.
 *
 * @param panel - The panel to parse the file of.
 * @param artifactMap - A collection of all parsed artifacts, keyed by name.
 */
export function parseFilePanel(
  panel: CreatorFilePanel,
  artifactMap: ArtifactMap
): void {
  if (!panel.file) return;

  const [fileType = "", fileTargetType = ""] =
    panel.file.name?.split(".")[0]?.split("2") || [];

  const handleError = () => {
    panel.errorMessage = "Unable to parse this file";
  };

  if (panel.variant === "artifact") {
    panel.type = panel.type || fileType;

    parseArtifactFile(panel.type, panel.file)
      .then(({ entities, errors }) => {
        panel.artifacts = entities;
        panel.errorMessage =
          errors.length === 0 ? undefined : errors.join(", ");
        panel.itemNames = entities.map(({ name }) => name);

        entities.forEach((artifact) => {
          artifactMap[artifact.name] = artifact;
        });
      })
      .catch(handleError);
  } else {
    panel.type = panel.type || fileType;
    panel.toType = panel.toType || fileTargetType;

    parseTraceFile(panel.file)
      .then(({ entities, errors }) => {
        panel.traces = entities;

        errors.push(...getTraceErrors(panel, artifactMap, entities));

        panel.errorMessage =
          errors.length === 0 ? undefined : errors.join(", ");
        panel.itemNames = entities.map(extractTraceId);
      })
      .catch(handleError);
  }
}

/**
 * Returns any errors for the given trace links.
 *
 * @param panel - The panel for uploading trace links.
 * @param artifactMap - A collection of all artifacts.
 * @param traces - The traces to check for errors.
 * @return The error message, if there is one.
 */
function getTraceErrors(
  panel: CreatorFilePanel,
  artifactMap: ArtifactMap,
  traces: TraceLinkSchema[]
): string[] {
  const errors: string[] = [];

  traces.forEach(({ sourceName, targetName }) => {
    if (!(sourceName in artifactMap)) {
      errors.push(`Artifact ${sourceName} does not exist`);
    } else if (!(targetName in artifactMap)) {
      errors.push(`Artifact ${targetName} does not exist`);
    } else {
      const sourceArtifact = artifactMap[sourceName];
      const targetArtifact = artifactMap[targetName];

      if (sourceArtifact.type !== panel.type) {
        errors.push(`${sourceArtifact.name} is not of type ${panel.type}`);
      }

      if (targetArtifact.type !== panel.toType) {
        errors.push(`${targetArtifact.name} is not of type ${panel.toType}`);
      }
    }
  });

  return errors;
}

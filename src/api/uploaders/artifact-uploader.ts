import {
  ArtifactMap,
  ArtifactModel,
  ParseArtifactFileModel,
  ArtifactFile,
  ArtifactPanel,
  ArtifactUploader,
} from "@/types";
import { logStore } from "@/hooks";
import { parseArtifactFile } from "@/api";

/**
 * Creates an artifact uploader.
 */
export function createArtifactUploader(): ArtifactUploader {
  return {
    panels: [],
    createNewPanel,
  };
}

/**
 * Creates a new uploader panel.
 *
 * @param artifactName - The title of the panel.
 */
function createNewPanel(artifactName: string): ArtifactPanel {
  return {
    title: artifactName,
    entityNames: [],
    projectFile: createArtifactFile(artifactName),
    getIsValid(): boolean {
      return isArtifactPanelValid(this);
    },
    clearPanel(): void {
      return clearPanel(this);
    },
    parseFile(artifactMap: ArtifactMap, file: File): Promise<void> {
      return createParsedArtifactFile(artifactMap, this, file);
    },
  };
}

/**
 * Creates a new artifact file.
 *
 * @param artifactType - The artifact type in this file.
 */
function createArtifactFile(artifactType: string): ArtifactFile {
  return {
    type: artifactType,
    file: undefined,
    artifacts: [],
    errors: [],
    isValid: false,
  };
}

/**
 * Returns whether the panel is valid.
 *
 * @param panel - The panel to check.
 * @return Whether it is valid.
 */
function isArtifactPanelValid(panel: ArtifactPanel): boolean {
  return (
    panel.projectFile.file !== undefined &&
    panel.projectFile.errors.length === 0
  );
}

/**
 * Clears the panel.
 *
 * @param panel - The panel to clear.
 */
function clearPanel(panel: ArtifactPanel): void {
  panel.projectFile = {
    ...panel.projectFile,
    file: undefined,
    artifacts: [],
    errors: [],
  };
  panel.entityNames = [];
}

/**
 * Parses the uploaded artifacts.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param panel - The artifact panel.
 * @param file - The file to parse.
 */
function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: ArtifactPanel,
  file: File
): Promise<void> {
  return parseArtifactFile(panel.projectFile.type, file)
    .then((res: ParseArtifactFileModel) => {
      const { entities, errors } = res;
      const validArtifacts: ArtifactModel[] = [];

      entities.forEach((artifact) => {
        const error = getArtifactError(artifactMap, artifact);

        if (error === undefined) {
          validArtifacts.push(artifact);
          artifactMap[artifact.name] = artifact;
        } else {
          errors.push(error);
        }
      });

      panel.projectFile = {
        ...panel.projectFile,
        artifacts: validArtifacts,
        errors,
        file,
      };
      panel.entityNames = entities.map(({ name }) => name);
    })
    .catch((e) => {
      logStore.onDevError(e);
      panel.projectFile.isValid = false;
      panel.projectFile.errors = ["Unable to parse file"];
    });
}

/**
 * Returns any errors for the given artifact.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param artifact - The artifact to check.
 * @return The error message, if there is one.
 */
function getArtifactError(
  artifactMap: ArtifactMap,
  artifact: ArtifactModel
): string | undefined {
  if (artifact.name in artifactMap) {
    return `Could not parse duplicate artifact: ${artifact.name}`;
  }
}

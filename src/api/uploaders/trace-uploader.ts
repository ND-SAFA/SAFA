import {
  ArtifactMap,
  ArtifactModel,
  IGenericUploader,
  LinkModel,
  ParseTraceFileModel,
  TraceFile,
  TraceLinkModel,
  TracePanel,
} from "@/types";
import { extractTraceId } from "@/util";
import { logStore } from "@/hooks";
import { parseTraceFile } from "@/api";

/**
 * Creates a trace file uploader.
 */
export function createTraceUploader(): IGenericUploader<
  ArtifactMap,
  LinkModel,
  TraceFile
> {
  return {
    panels: [],
    createNewPanel,
  };
}

/**
 * Creates a new uploader panel.
 *
 * @param traceLink - The like to create the panel for.
 */
function createNewPanel(traceLink: LinkModel): TracePanel {
  return {
    title: `${traceLink.sourceName} X ${traceLink.targetName}`,
    entityNames: [],
    projectFile: createTraceFile(traceLink),
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
 * Creates a new trace file.
 *
 * @param traceLink - The trace link in this file.
 */
function createTraceFile(traceLink: LinkModel): TraceFile {
  return {
    sourceId: traceLink.sourceId,
    targetId: traceLink.targetId,
    isGenerated: false,
    isValid: false,
    errors: [],
    traces: [],
  };
}

/**
 * Returns whether the panel is valid.
 *
 * @param panel - The panel to check.
 * @return Whether it is valid.
 */
function isArtifactPanelValid(panel: TracePanel): boolean {
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
function clearPanel(panel: TracePanel): void {
  panel.projectFile = {
    ...panel.projectFile,
    file: undefined,
    traces: [],
    errors: [],
  };
  panel.entityNames = [];
}

/**
 * Parses the uploaded trace links.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param panel - The trace panel.
 * @param file - The file to parse.
 */
function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: TracePanel,
  file: File
): Promise<void> {
  return parseTraceFile(file)
    .then((res: ParseTraceFileModel) => {
      const { entities, errors } = res;
      const validTraces: TraceLinkModel[] = [];

      entities.forEach((link) => {
        const error = getTraceError(panel.projectFile, artifactMap, link);

        if (error === undefined) {
          validTraces.push(link);
        } else {
          errors.push(error);
        }
      });

      panel.projectFile.traces = validTraces;
      panel.projectFile.errors = errors;
      panel.projectFile.file = file;
      panel.entityNames = entities.map(extractTraceId);
    })
    .catch((e) => {
      logStore.onDevError(e);
      panel.projectFile.isValid = false;
      panel.projectFile.errors = ["Unable to parse file"];
    });
}

/**
 * Returns any errors for the given trace link.
 *
 * @param traceFile - The trace file.
 * @param artifactMap - A collection of all artifacts.
 * @param traceLink - The trace to check.
 * @return The error message, if there is one.
 */
function getTraceError(
  traceFile: TraceFile,
  artifactMap: Record<string, ArtifactModel>,
  traceLink: LinkModel
): string | undefined {
  const { sourceName, targetName } = traceLink;

  if (!(sourceName in artifactMap)) {
    return `Artifact ${sourceName} does not exist.`;
  } else if (!(targetName in artifactMap)) {
    return `Artifact ${targetName} does not exist.`;
  } else {
    const sourceArtifact = artifactMap[sourceName];
    const targetArtifact = artifactMap[targetName];

    if (sourceArtifact.type !== traceFile.sourceId) {
      return `${sourceArtifact.name} is not of type ${traceFile.sourceId}.`;
    }

    if (targetArtifact.type !== traceFile.targetId) {
      return `${targetArtifact.name} is not of type ${traceFile.targetId}.`;
    }
  }
}

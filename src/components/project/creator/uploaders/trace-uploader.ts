import { parseTraceFile, generateLinks } from "@/api";
import {
  ArtifactMap,
  IGenericUploader,
  Artifact,
  TraceFile,
  ParseTraceFileResponse,
  Link,
  TraceLink,
  TracePanel,
} from "@/types";

const DEFAULT_IS_GENERATED = false;
const testPanels = [
  createNewPanel({ source: "Requirements", target: "Hazards" }),
  createNewPanel({ source: "Designs", target: "Requirements" }),
];
export function createTraceUploader(): IGenericUploader<
  ArtifactMap,
  Link,
  TraceFile
> {
  return {
    panels: testPanels,
    createNewPanel,
  };
}

function createNewPanel(traceLink: Link): TracePanel {
  const emptyArtifactFile: TraceFile = createTraceFile(traceLink);
  return {
    title: getTraceId(traceLink),
    entityNames: [],
    projectFile: emptyArtifactFile,
    getIsValid(): boolean {
      return isArtifactPanelValid(this);
    },
    clearPanel(): void {
      return clearPanel(this);
    },
    parseFile(artifactMap: ArtifactMap, file: File): Promise<void> {
      return createParsedArtifactFile(artifactMap, this, file);
    },
    generateTraceLinks(artifactMap: ArtifactMap): Promise<void> {
      return generateTraceLinks(artifactMap, this);
    },
  };
}

function generateTraceLinks(
  artifactMap: ArtifactMap,
  tracePanel: TracePanel
): Promise<void> {
  const sourceType = tracePanel.projectFile.source;
  const targetType = tracePanel.projectFile.target;
  const artifacts: Artifact[] = Object.values(artifactMap);
  const sourceArtifacts: Artifact[] = artifacts.filter(
    (a) => a.type === sourceType
  );
  const targetArtifacts: Artifact[] = artifacts.filter(
    (a) => a.type === targetType
  );

  return generateLinks(sourceArtifacts, targetArtifacts).then((traceLinks) => {
    tracePanel.projectFile.traces = traceLinks;
    tracePanel.entityNames = traceLinks.map(getTraceId);
  });
}

function createTraceFile(traceLink: Link): TraceFile {
  return {
    source: traceLink.source,
    target: traceLink.target,
    isGenerated: DEFAULT_IS_GENERATED,
    isValid: false,
    errors: [],
    traces: [],
  };
}

function isArtifactPanelValid(panel: TracePanel): boolean {
  return (
    panel.projectFile.file !== undefined &&
    panel.projectFile.errors.length === 0
  );
}

function clearPanel(panel: TracePanel): void {
  panel.projectFile = {
    ...panel.projectFile,
    file: undefined,
    traces: [],
    errors: [],
  };
  panel.entityNames = [];
}

function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: TracePanel,
  file: File
): Promise<void> {
  return parseTraceFile(file).then((res: ParseTraceFileResponse) => {
    const { traces, errors } = res;
    const validTraces: TraceLink[] = [];
    traces.forEach((t) => {
      const error = getTraceError(panel.projectFile, artifactMap, t);
      if (error === undefined) {
        validTraces.push(t);
      } else {
        errors.push(error);
      }
    });

    panel.projectFile.traces = validTraces;
    panel.projectFile.errors = errors;
    panel.projectFile.file = file;
    panel.entityNames = traces.map(getTraceId);
  });
}

function getTraceId(traceLink: Link): string {
  return `${traceLink.source}-${traceLink.target}`;
}

function getTraceError(
  traceFile: TraceFile,
  artifactMap: Record<string, Artifact>,
  traceLink: Link
): string | undefined {
  const { source, target } = traceLink;
  if (!(source in artifactMap)) {
    return `Artifact ${source} does not exist.`;
  } else if (!(target in artifactMap)) {
    return `Artifact ${target} does not exist.`;
  } else {
    const sourceArtifact = artifactMap[source];
    const targetArtifact = artifactMap[target];

    if (sourceArtifact.type !== traceFile.source) {
      return `${sourceArtifact.name} is not of type ${traceFile.source}.`;
    }

    if (targetArtifact.type !== traceFile.target) {
      return `${targetArtifact.name} is not of type ${traceFile.target}.`;
    }
  }
}

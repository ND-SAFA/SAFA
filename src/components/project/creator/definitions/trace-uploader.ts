import { parseTraceFile } from "@/api/parse-api";
import { ParseTraceFileResponse } from "@/types/api";
import { TraceFile } from "@/types/common-components";
import { Artifact } from "@/types/domain/artifact";
import { Link, TraceLink } from "@/types/domain/links";
import { ArtifactMap, IGenericFilePanel, IGenericUploader } from "./types";

const DEFAULT_IS_GENERATED = false;
type TracePanel = IGenericFilePanel<ArtifactMap, TraceFile>;

export function createTraceUploader(): IGenericUploader<
  ArtifactMap,
  Link,
  TraceFile
> {
  return {
    panels: [],
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
  };
}

function createTraceFile(traceLink: Link): TraceFile {
  return {
    source: traceLink.source,
    target: traceLink.target,
    isGenerated: DEFAULT_IS_GENERATED,
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

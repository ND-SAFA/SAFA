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
    panels: [
      createNewPanel({
        source: "Requirements",
        target: "Requirements",
      }),
    ],
    createNewPanel(traceLink: Link): TracePanel {
      return createNewPanel(traceLink);
    },
  };
}

function createNewPanel(traceLink: Link): TracePanel {
  const emptyArtifactFile: TraceFile = createTraceFile(traceLink);
  const newPanel: TracePanel = {
    title: getTraceId(traceLink),
    entityNames: [],
    projectFile: emptyArtifactFile,
    getIsValid(): boolean {
      return isArtifactPanelValid(this);
    },
    clearFile(): TracePanel {
      return clearPanelFile(this);
    },
    parseFile(artifactMap: ArtifactMap, file: File): Promise<TracePanel> {
      return createParsedArtifactFile(artifactMap, this, file);
    },
  };
  return newPanel;
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

function clearPanelFile(panel: TracePanel): TracePanel {
  const updatedFile: TraceFile = {
    ...panel.projectFile,
    file: undefined,
    traces: [],
    errors: [],
  };
  return {
    ...panel,
    projectFile: updatedFile,
    entityNames: [],
  };
}

function createParsedArtifactFile(
  artifactMap: ArtifactMap,
  panel: TracePanel,
  file: File
): Promise<TracePanel> {
  return new Promise((resolve, reject) => {
    const { projectFile } = panel;
    parseTraceFile(file)
      .then((res: ParseTraceFileResponse) => {
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
        const updatedFile: TraceFile = {
          ...projectFile,
          traces: validTraces,
          errors,
          file,
        };

        const updatedPanel: TracePanel = {
          ...panel,
          entityNames: traces.map(getTraceId),
          projectFile: updatedFile,
        };

        resolve(updatedPanel);
      })
      .catch(reject);
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

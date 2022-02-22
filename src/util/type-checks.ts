import { Artifact, EntityModification } from "@/types/domain";
import {
  IGenericFilePanel,
  ProjectFile,
  TraceFile,
  TracePanel,
} from "@/types/components";

/**
 * Returns whether the given ArtifactDelta is an modified artifact.
 *
 * @param artifact - The artifact to check.
 *
 * @return Whether this item is an modified artifact.
 */
export function isModifiedArtifact(
  artifact: any
): artifact is EntityModification<Artifact> {
  return "before" in artifact && "after" in artifact;
}

export function isArtifact(obj: any): obj is Artifact {
  return "id" in obj && "summary" in obj && "body" in obj && "type" in obj;
}

/**
 * Determines whether this project file is a trace file.
 *
 * @param file - The project file to check.
 *
 * @return Whether this file is a trace file.
 */
export function isTraceFile(file: ProjectFile): file is TraceFile {
  return (
    "source" in file &&
    "target" in file &&
    "isGenerated" in file &&
    "traces" in file
  );
}

/**
 * Determines whether this panel is a trace panel.
 *
 * @param panel - The panel to check.
 *
 * @return Whether this panel is a trace panel.
 */
export function isTracePanel(
  panel: IGenericFilePanel<any, any>
): panel is TracePanel {
  return isTraceFile(panel.projectFile);
}

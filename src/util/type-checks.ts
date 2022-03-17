import { Artifact, ArtifactData, EntityModification } from "@/types/domain";
import {
  IGenericFilePanel,
  ProjectFile,
  TraceFile,
  TracePanel,
} from "@/types/components";

/**
 * Returns whether the given ArtifactDelta is an modified artifact.
 *
 * @param obj - The artifact to check.
 *
 * @return Whether this item is an modified artifact.
 */
export function isModifiedArtifact(
  obj: any
): obj is EntityModification<Artifact> {
  const requiredFields = ["before", "after"];
  return containsFields(obj, requiredFields);
}

export function isArtifact(obj: any): obj is Artifact {
  const requiredFields = ["id", "summary", "body", "type"];
  return containsFields(obj, requiredFields);
}

export function isArtifactData(obj: any): obj is ArtifactData {
  const requiredFields = [
    "body",
    "artifactName",
    "artifactType",
    "artifactDeltaState",
    "isSelected",
    "opacity",
  ];
  return containsFields(obj, requiredFields);
}

function containsFields(obj: any, fields: string[]): boolean {
  return fields
    .map((field) => field in obj)
    .reduce((prev, curr) => prev && curr, true);
}

/**
 * Determines whether this project file is a trace file.
 *
 * @param file - The project file to check.
 *
 * @return Whether this file is a trace file.
 */
export function isTraceFile(file: ProjectFile): file is TraceFile {
  const requiredFields = ["sourceId", "targetId", "isGenerated", "traces"];
  return containsFields(file, requiredFields);
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

import {
  ArtifactSchema,
  ArtifactData,
  DeltaArtifact,
  EntityModification,
  IGenericFilePanel,
  ProjectFile,
  TraceFile,
  TracePanel,
} from "@/types";

/**
 * Returns whether the given artifact or delta is a modified artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is a modified artifact.
 */
export function isModifiedArtifact(
  artifact: DeltaArtifact
): artifact is EntityModification<ArtifactSchema> {
  const requiredFields = ["before", "after"];
  return containsFields(artifact, requiredFields);
}

/**
 * Returns whether the given artifact or delta is an artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is an artifact.
 */
export function isArtifact(
  artifact: DeltaArtifact
): artifact is ArtifactSchema {
  const requiredFields = ["id", "body", "type"];
  return containsFields(artifact, requiredFields);
}

/**
 * Returns whether the given cytoscape data is an artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is an artifact.
 */
export function isArtifactData(artifact: unknown): artifact is ArtifactData {
  const requiredFields = [
    "body",
    "artifactName",
    "artifactType",
    "artifactDeltaState",
    "isSelected",
    "opacity",
  ];
  return containsFields(artifact, requiredFields);
}

/**
 * Returns whether an object contains certain fields.
 *
 * @param object - The object to check.
 * @param fields - The fields required to exist on the object.
 * @return Whether this object has all required fields.
 */
function containsFields(object: unknown, fields: string[]): boolean {
  return fields
    .map((field) => field in (object as Record<string, unknown>))
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
  panel: IGenericFilePanel<Record<string, unknown>, ProjectFile>
): panel is TracePanel {
  return isTraceFile(panel.projectFile);
}

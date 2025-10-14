import {
  ArtifactSchema,
  ArtifactCytoElementData,
  ArtifactDeltaSchema,
  EntityModificationSchema,
} from "@/types";

/**
 * Returns whether the given artifact or delta is a modified artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is a modified artifact.
 */
export function isModifiedArtifact(
  artifact: ArtifactDeltaSchema
): artifact is EntityModificationSchema<ArtifactSchema> {
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
  artifact: ArtifactDeltaSchema
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
export function isArtifactData(
  artifact: unknown
): artifact is ArtifactCytoElementData {
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

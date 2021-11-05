import {
  AddedArtifact,
  APIError,
  APIResponse,
  DeltaArtifact,
  DeltaType,
  ModifiedArtifact,
  ProjectFile,
  RemovedArtifact,
  TraceFile,
} from "@/types";

/**
 * Returns whether the given value is an API error.
 *
 * @param blob - The response to check.
 *
 * @return Whether this item is an error.
 */
export function isAPIError<T>(
  blob: APIResponse<T> | APIError
): blob is APIError {
  return blob.status > 0;
}

/**
 * Returns whether the given value is an added artifact.
 *
 * @param artifact - The artifact to check.
 *
 * @return Whether this item is an added artifact.
 */
export function isAddedArtifact(
  artifact: DeltaArtifact
): artifact is AddedArtifact {
  return "after" in artifact && !("before" in artifact);
}

/**
 * Returns whether the given value is an removed artifact.
 *
 * @param artifact - The artifact to check.
 *
 * @return Whether this item is an removed artifact.
 */
export function isRemovedArtifact(
  artifact: DeltaArtifact
): artifact is RemovedArtifact {
  return "before" in artifact && !("after" in artifact);
}
/**
 * Returns whether the given value is an modified artifact.
 *
 * @param artifact - The artifact to check.
 *
 * @return Whether this item is an modified artifact.
 */
export function isModifiedArtifact(
  artifact: DeltaArtifact
): artifact is ModifiedArtifact {
  return "before" in artifact && "after" in artifact;
}

/**
 * Returns the delta type of of the given artifact.
 *
 * @param artifact - The artifact to check.
 *
 * @return The corresponding delta type.
 */
export function getDeltaType(artifact: DeltaArtifact): DeltaType {
  if (isAddedArtifact(artifact)) return "added";
  if (isModifiedArtifact(artifact)) return "modified";
  if (isRemovedArtifact(artifact)) return "removed";
  else
    throw Error(
      "Unrecognized artifact delta state: " + JSON.stringify(artifact)
    );
}

/**
 * Determines whether this project file is a trace file.
 *
 * @param file - The project file to check.
 *
 * @return Whether this file is a trace file.
 */
export function isTraceFile(file: ProjectFile): file is TraceFile {
  return "isGenerated" in file;
}

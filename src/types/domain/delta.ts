export enum ArtifactDeltaState {
  NO_CHANGE = "no_change",
  MODIFIED = "modified",
  ADDED = "added",
  REMOVED = "removed",
}

export interface AddedArtifact {
  after: string;
}

export interface RemovedArtifact {
  before: string;
}

export interface ModifiedArtifact {
  before: string;
  after: string;
}

export type DeltaArtifact = AddedArtifact | RemovedArtifact | ModifiedArtifact;

export function isAddedArtifact(
  artifact: DeltaArtifact
): artifact is AddedArtifact {
  return "after" in artifact && !("before" in artifact);
}

export function isRemovedArtifact(
  artifact: DeltaArtifact
): artifact is RemovedArtifact {
  return "before" in artifact && !("after" in artifact);
}

export function isModifiedArtifact(
  artifact: DeltaArtifact
): artifact is ModifiedArtifact {
  return "before" in artifact && "after" in artifact;
}

export type DeltaType = "added" | "modified" | "removed";

export function getDeltaType(artifact: DeltaArtifact): DeltaType {
  if (isAddedArtifact(artifact)) return "added";
  if (isModifiedArtifact(artifact)) return "modified";
  if (isRemovedArtifact(artifact)) return "removed";
  else
    throw Error(
      "Unrecognized artifact delta state: " + JSON.stringify(artifact)
    );
}

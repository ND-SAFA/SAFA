import {
  allowedSafetyCaseTypes,
  ApprovalType,
  ArtifactData,
  ArtifactModel,
  ArtifactTypeDirections,
  LinkModel,
  TraceLinkModel,
  TraceType,
} from "@/types";

/**
 * Returns the trace ID made from the given source and target IDs.
 *
 * @param source - The source ID.
 * @param target - THe target ID.
 * @return The standardized ID of the source joined to the target.
 */
export function getTraceId(source: string, target: string): string {
  return `${source}-${target}`;
}

/**
 * Returns the trace ID made from the given source and target IDs.
 *
 * @param traceLink - The trace link.
 * @return The standardized ID of the source joined to the target.
 */
export function extractTraceId(traceLink: LinkModel): string {
  return `${traceLink.sourceName}-${traceLink.targetName}`;
}

/**
 * Creates a predicate for matching a trace.
 *
 * @param sourceId - The source to match.
 * @param targetId - The target to match.
 * @param ignoreDirection - If true, will match traces in both directions.
 * @return A predicate for finding matching links.
 */
export function matchTrace(
  sourceId: string,
  targetId: string,
  ignoreDirection = false
) {
  return (trace: TraceLinkModel): boolean =>
    ignoreDirection
      ? (trace.sourceId === sourceId && trace.targetId === targetId) ||
        (trace.targetId === sourceId && trace.sourceId === targetId)
      : trace.sourceId === sourceId && trace.targetId === targetId;
}

/**
 * Determines if the trace link is allowed based on the type of the nodes.
 *
 * @param source - The source artifact.
 * @param target - The target artifact.
 * @param artifactTypeDirections - The allowed directions of traces.
 * @return Whether the link is allowed.
 */
export function isLinkAllowedByType(
  source: ArtifactModel | ArtifactData,
  target: ArtifactModel | ArtifactData,
  artifactTypeDirections: ArtifactTypeDirections
): boolean {
  const sourceType =
    "artifactType" in source ? source.artifactType : source.type;
  const targetType =
    "artifactType" in target ? target.artifactType : target.type;
  const isSourceDefaultArtifact = !source.safetyCaseType && !source.logicType;
  const isTargetDefaultArtifact = !target.safetyCaseType && !target.logicType;

  if (isSourceDefaultArtifact) {
    return !artifactTypeDirections[targetType]?.includes(sourceType);
  } else if (source.safetyCaseType) {
    if (isTargetDefaultArtifact) return true;
    if (target.logicType || !target.safetyCaseType) return false;

    return allowedSafetyCaseTypes[source.safetyCaseType].includes(
      target.safetyCaseType
    );
  } else if (source.logicType) {
    return isTargetDefaultArtifact;
  }

  return false;
}

/**
 * Returns helper functions for determining a link's status.
 *
 * @param traceLink - The link to check.
 * @return Status callbacks.
 */
export function linkStatus(traceLink?: TraceLinkModel) {
  const canBeModified = () => traceLink?.traceType === TraceType.GENERATED;

  return {
    canBeModified,
    canBeDeleted: () => !canBeModified(),
    canBeApproved: () =>
      canBeModified() && traceLink?.approvalStatus !== ApprovalType.APPROVED,
    canBeDeclined: () =>
      canBeModified() && traceLink?.approvalStatus !== ApprovalType.DECLINED,
    canBeReset: () =>
      canBeModified() && traceLink?.approvalStatus !== ApprovalType.UNREVIEWED,
  };
}

import {
  ArtifactCytoElementData,
  ArtifactSchema,
  LinkSchema,
  TraceLinkSchema,
  TraceMatrixSchema,
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
export function extractTraceId(traceLink: LinkSchema): string {
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
  return (trace: TraceLinkSchema): boolean =>
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
 * @param traceMatrices - The existing links between types.
 * @return Whether the link is allowed.
 */
export function isLinkAllowedByType(
  source: ArtifactSchema | ArtifactCytoElementData,
  target: ArtifactSchema | ArtifactCytoElementData,
  traceMatrices: TraceMatrixSchema[]
): boolean {
  const sourceType =
    "artifactType" in source ? source.artifactType : source.type;
  const targetType =
    "artifactType" in target ? target.artifactType : target.type;

  return sourceType === targetType
    ? true
    : !traceMatrices.find(
        (matrix) =>
          matrix.sourceType === targetType && matrix.targetType === sourceType
      );
}

/**
 * Returns helper functions for determining a link's status.
 *
 * @param traceLink - The link to check.
 * @return Status callbacks.
 */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function linkStatus(traceLink?: TraceLinkSchema) {
  const canBeModified = () => traceLink?.traceType === "GENERATED";

  return {
    canBeModified,
    canBeApproved: () =>
      canBeModified() && traceLink?.approvalStatus !== "APPROVED",
    canBeDeclined: () =>
      canBeModified() && traceLink?.approvalStatus !== "DECLINED",
    canBeReset: () =>
      canBeModified() && traceLink?.approvalStatus !== "UNREVIEWED",
  };
}

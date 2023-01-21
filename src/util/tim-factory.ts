import { ApprovalType, ProjectSchema, TimSchema, TraceType } from "@/types";

/**
 * @return A project TIM structure initialized to the given values.
 */
export function createTIM(project?: ProjectSchema): TimSchema {
  const delimiter = `~~~`;
  const artifactCounts: Record<string, number> = {};
  const artifactTypes: Record<string, string> = {};
  const traceCounts: Record<
    string,
    { total: number; generated: number; approved: number }
  > = {};

  project?.artifacts.forEach(({ id, type }) => {
    artifactCounts[type] = (artifactCounts[type] || 0) + 1;
    artifactTypes[id] = type;
  });

  project?.traces.forEach(
    ({ sourceId, targetId, approvalStatus, traceType }) => {
      const type = `${artifactTypes[sourceId]}${delimiter}${artifactTypes[targetId]}`;
      const currentTotal = traceCounts[type]?.total || 0;
      const currentGenerated = traceCounts[type]?.generated || 0;
      const currentApproved = traceCounts[type]?.approved || 0;
      const isGenerated = traceType === TraceType.GENERATED;
      const isApproved =
        isGenerated && approvalStatus === ApprovalType.APPROVED;

      traceCounts[type] = {
        total: currentTotal + 1,
        generated: isGenerated ? currentGenerated + 1 : currentGenerated,
        approved: isApproved ? currentApproved + 1 : currentApproved,
      };
    }
  );

  return {
    artifacts: Object.entries(artifactCounts).map(([artifactType, count]) => ({
      artifactType,
      count,
    })),
    traces: Object.entries(traceCounts).map(([sourceAndTargetType, count]) => ({
      sourceType: sourceAndTargetType.split(delimiter)[0],
      targetType: sourceAndTargetType.split(delimiter)[1],
      count: count.total,
      generatedCount: count.generated,
      approvedCount: count.approved,
    })),
  };
}

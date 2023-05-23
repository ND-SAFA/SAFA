import { ApprovalType, ProjectSchema, TimSchema, TraceType } from "@/types";
import { defaultTypeIcon } from "@/util/icons";
import { getTypeColor } from "@/util/theme";

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

  // Add trace counts from the artifact types, in case a type direction exists with 0 links.
  Object.entries(project?.typeDirections || {}).forEach(
    ([name, allowedTypes]) => {
      allowedTypes.forEach((allowedType) => {
        const type = `${name}${delimiter}${allowedType}`;

        traceCounts[type] = {
          total: 0,
          generated: 0,
          approved: 0,
        };
      });
    }
  );

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
    artifacts: Object.entries(artifactCounts)
      .map(([artifactType, count]) => ({
        [artifactType]: {
          typeId:
            project?.artifactTypes.find(({ name }) => name === artifactType)
              ?.typeId || artifactType,
          name: artifactType,
          count,
          icon: defaultTypeIcon,
          allowedTypes: project?.typeDirections[artifactType] || [],
          iconIndex: 0,
          color: getTypeColor(artifactType),
        },
      }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
    traces: Object.entries(traceCounts).map(([sourceAndTargetType, count]) => ({
      sourceType: sourceAndTargetType.split(delimiter)[0],
      targetType: sourceAndTargetType.split(delimiter)[1],
      count: count.total,
      generatedCount: count.generated,
      approvedCount: count.approved,
    })),
  };
}

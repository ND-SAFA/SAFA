import { ProjectSchema, TimStructure } from "@/types";

/**
 * @return A project TIM structure initialized to the given values.
 */
export function createTIM(project: ProjectSchema): TimStructure {
  const delimiter = `~~~`;
  const artifactCounts: Record<string, number> = {};
  const artifactTypes: Record<string, string> = {};
  const traceCounts: Record<string, number> = {};

  project.artifacts.forEach(({ id, type }) => {
    if (!artifactCounts[type]) {
      artifactCounts[type] = 1;
    } else {
      artifactCounts[type] += 1;
    }

    artifactTypes[id] = type;
  });

  project.traces.forEach(({ sourceId, targetId }) => {
    const type = `${artifactTypes[sourceId]}${delimiter}${artifactTypes[targetId]}`;

    if (!traceCounts[type]) {
      traceCounts[type] = 1;
    } else {
      traceCounts[type] += 1;
    }
  });

  return {
    artifacts: Object.entries(artifactCounts).map(([artifactType, count]) => ({
      artifactType,
      count,
    })),
    traces: Object.entries(traceCounts).map(([sourceAndTargetType, count]) => ({
      source: sourceAndTargetType.split(delimiter)[0],
      target: sourceAndTargetType.split(delimiter)[1],
      count,
    })),
  };
}

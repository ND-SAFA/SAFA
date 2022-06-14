import { NodeSingular } from "cytoscape";
import { ArtifactData, SafetyCaseType } from "@/types";
import { traceModule, typeOptionsModule } from "@/store";

/**
 * Return whether any two nodes can be traced. Criteria includes:
 * - source != target.
 * - trace link between source and target doesn't already exist.
 *
 * @param sourceNode - The source node on the graph.
 * @param targetNode - The target node on the graph.
 * @returns Whether the two nodes can be traced.
 */
export function canConnect(
  sourceNode: NodeSingular,
  targetNode: NodeSingular
): boolean {
  if (sourceNode.data() === undefined || targetNode.data() === undefined) {
    // If either link doesn't have any data, the link cannot be created.
    return false;
  }

  const sourceData: ArtifactData = sourceNode.data();
  const targetData: ArtifactData = targetNode.data();

  // If this link already exists, the link cannot be created.
  const linkDoesNotExist = !traceModule.doesLinkExist(
    sourceData.id,
    targetData.id
  );

  // If this link in opposite direct exists, the link cannot be created.
  const oppositeLinkDoesNotExist = !traceModule.doesLinkExist(
    targetData.id,
    sourceData.id
  );

  // If this link is to itself, the link cannot be created.
  const isNotSameNode = !sourceNode.same(targetNode);

  // If the link is not between allowed artifact directions, thee link cannot be created.
  const linkIsAllowedByType = artifactTypesAreValid(sourceData, targetData);

  return (
    linkDoesNotExist &&
    isNotSameNode &&
    oppositeLinkDoesNotExist &&
    linkIsAllowedByType
  );
}

const allowedSafetyCaseTypes: Record<SafetyCaseType, SafetyCaseType[]> = {
  [SafetyCaseType.GOAL]: [SafetyCaseType.GOAL, SafetyCaseType.STRATEGY],
  [SafetyCaseType.SOLUTION]: [SafetyCaseType.GOAL],
  [SafetyCaseType.CONTEXT]: [SafetyCaseType.GOAL],
  [SafetyCaseType.STRATEGY]: [SafetyCaseType.GOAL],
};

export type ArtifactIdentifierInformation = Pick<
  ArtifactData,
  "safetyCaseType" | "logicType" | "artifactType" | "type"
>;
/**
 * Returns whether given artifact can traced regarding their artifact types
 * rules.
 * @param sourceData The artifact data of the source artifact.
 * @param targetData The artifact data of the target artifact.
 */
export function artifactTypesAreValid(
  sourceData: ArtifactIdentifierInformation,
  targetData: ArtifactIdentifierInformation
): boolean {
  const isSourceDefaultArtifact =
    !sourceData.safetyCaseType && !sourceData.logicType;
  const isTargetDefaultArtifact =
    !targetData.safetyCaseType && !targetData.logicType;

  if (isSourceDefaultArtifact) {
    return typeOptionsModule.isLinkAllowedByType(
      sourceData.artifactType,
      targetData.artifactType
    );
  } else if (sourceData.safetyCaseType) {
    if (isTargetDefaultArtifact) return true;
    if (targetData.logicType) return false;

    const sourceSafetyCaseType: SafetyCaseType =
      SafetyCaseType[sourceData.safetyCaseType as keyof typeof SafetyCaseType];
    const targetSafetyCaseType: SafetyCaseType =
      SafetyCaseType[targetData.safetyCaseType as keyof typeof SafetyCaseType];

    const allowedTypes = allowedSafetyCaseTypes[sourceSafetyCaseType];
    return allowedTypes.includes(targetSafetyCaseType);
  } else if (sourceData.logicType) {
    return isTargetDefaultArtifact;
  }

  throw Error("Undefined trace link logic for:" + sourceData.type);
}

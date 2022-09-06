import { NodeSingular } from "cytoscape";
import { ArtifactData } from "@/types";
import { traceStore } from "@/hooks";

/**
 * Return whether any two nodes can be traced.
 *
 * @param sourceNode - The source node on the graph.
 * @param targetNode - The target node on the graph.
 * @returns Whether the two nodes can be traced.
 */
export function canConnect(
  sourceNode: NodeSingular,
  targetNode: NodeSingular
): boolean {
  const sourceData: ArtifactData | undefined = sourceNode.data();
  const targetData: ArtifactData | undefined = targetNode.data();

  if (!sourceData || !targetData) return false;

  return traceStore.isLinkAllowed(sourceData, targetData) === true;
}

import { NodeSingular } from "cytoscape";
import { ArtifactCytoElementData } from "@/types";
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
  const sourceData: ArtifactCytoElementData | undefined = sourceNode.data();
  const targetData: ArtifactCytoElementData | undefined = targetNode.data();

  if (!sourceData || !targetData) return false;

  return traceStore.isLinkAllowed(sourceData, targetData) === true;
}

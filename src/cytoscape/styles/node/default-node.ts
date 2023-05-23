import { ArtifactCytoElementData } from "@/types";
import { getTypeColor } from "@/util";
import { svgRect } from "./node-shapes";
import { svgNode } from "./svg-node";

/**
 * Creates the default SVG node.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
export function svgDefault(data: ArtifactCytoElementData): string {
  const outer = { width: 206, height: 160 };

  return svgNode(
    data,
    {
      marginTop: 6,
      truncateLength: 90,
      outer,
      inner: { x: 12, y: 20, width: 180, height: 100 },
    },
    svgRect(outer, 8, getTypeColor(data.artifactType))
  );
}

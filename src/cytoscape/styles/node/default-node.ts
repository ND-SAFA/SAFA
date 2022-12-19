import { ArtifactData } from "@/types";
import { getBackgroundColor, getBorderColor } from "@/util";
import { svgRect } from "./node-shapes";
import { svgNode } from "./svg-node";

/**
 * Creates the SVG safety case context.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
export function svgDefault(data: ArtifactData): string {
  const outer = { width: 206, height: 160 };

  return svgNode(
    data,
    {
      marginTop: 6,
      truncateLength: 90,
      outer,
      inner: { x: 10, y: 20, width: 180, height: 100 },
    },
    svgRect(
      outer,
      getBorderColor(data.artifactDeltaState),
      getBackgroundColor(data.artifactDeltaState, data.dark),
      8
    )
  );
}

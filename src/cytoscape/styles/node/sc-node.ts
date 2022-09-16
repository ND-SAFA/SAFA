import { ArtifactData } from "@/types";
import { getBackgroundColor, getBorderColor } from "@/util";
import { ARTIFACT_BORDER_WIDTH } from "@/cytoscape";
import { svgCircle, svgRect, svgRhombus } from "./node-shapes";
import { svgDefault } from "./default-node";
import { svgNode } from "./svg-node";

/**
 * Creates the HTML for representing a safety case node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
export function svgSafetyCase(data: ArtifactData): string {
  switch (data.safetyCaseType) {
    case "GOAL":
      return svgGoal(data);
    case "CONTEXT":
      return svgDefault(data);
    case "SOLUTION":
      return svgSolution(data);
    case "STRATEGY":
      return svgStrategy(data);
    default:
      return svgDefault(data);
  }
}

/**
 * Creates the SVG safety case goal.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgGoal(data: ArtifactData): string {
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
      getBackgroundColor(data.artifactDeltaState)
    )
  );
}

/**
 * Creates the SVG safety case solution.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgSolution(data: ArtifactData): string {
  const radius = 92;

  return svgNode(
    data,
    {
      marginTop: 7,
      truncateLength: 60,
      bodyWidth: 120,
      outer: { width: 200, height: 200 },
      inner: { x: 40, y: 35, width: 120, height: 82 },
    },
    svgCircle(
      radius,
      getBorderColor(data.artifactDeltaState),
      getBackgroundColor(data.artifactDeltaState)
    )
  );
}

/**
 * Creates the SVG safety case strategy.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgStrategy(data: ArtifactData): string {
  const outerHeight = 160;
  const outerWidth = 206;
  const xOffset = 20;

  return svgNode(
    data,
    {
      marginTop: 6,
      truncateLength: 90,
      outer: { width: outerWidth + xOffset, height: outerHeight },
      inner: { x: 30, y: 20, width: 180, height: 100 },
    },
    svgRhombus(
      { width: outerWidth, height: outerHeight },
      xOffset,
      getBorderColor(data.artifactDeltaState),
      getBackgroundColor(data.artifactDeltaState)
    )
  );
}

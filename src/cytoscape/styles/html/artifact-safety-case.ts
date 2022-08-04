import { ArtifactData } from "@/types";
import { getBackgroundColor, ThemeColors } from "@/util";
import { svgNode } from "./core-svg";
import { ARTIFACT_BORDER_WIDTH } from "@/cytoscape";

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
 * Creates the SVG safety case context.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
export function svgDefault(data: ArtifactData): string {
  const outerHeight = 160;
  const outerWidth = 206;

  return svgNode(
    data,
    { width: outerWidth, height: outerHeight, marginTop: 6 },
    { x: 10, y: 20, width: 180, height: 100, truncateLength: 90 },
    `
      <rect 
        rx="8" width="${outerWidth}" height="${outerHeight}"
        fill="${ThemeColors.darkGrey}"
        class="artifact-border"
      />
      <rect
        x="${ARTIFACT_BORDER_WIDTH}" y="${ARTIFACT_BORDER_WIDTH}" rx="7" 
        width="${outerWidth - ARTIFACT_BORDER_WIDTH * 2}" 
        height="${outerHeight - ARTIFACT_BORDER_WIDTH * 2}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
        class="artifact-svg"
      />
    `
  );
}

/**
 * Creates the SVG safety case goal.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgGoal(data: ArtifactData): string {
  const outerHeight = 160;
  const outerWidth = 206;

  return svgNode(
    data,
    {
      width: outerWidth,
      height: outerHeight,
      marginTop: 6,
    },
    { x: 10, y: 20, width: 180, height: 100, truncateLength: 90 },
    `
      <rect 
        width="${outerWidth}" height="${outerHeight}"
        fill="${ThemeColors.darkGrey}"
        class="artifact-border"
      />
      <rect
          x="${ARTIFACT_BORDER_WIDTH}" y="${ARTIFACT_BORDER_WIDTH}"
        width="${outerWidth - ARTIFACT_BORDER_WIDTH * 2}" 
        height="${outerHeight - ARTIFACT_BORDER_WIDTH * 2}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
        class="artifact-svg"
      />
    `
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
    { width: 200, height: 200, marginTop: 7 },
    {
      x: 40,
      y: 35,
      width: 120,
      height: 82,
      bodyWidth: 120,
      truncateLength: 60,
    },
    `
      <circle 
        cx="100" cy="100" r="${radius}"
        fill="${ThemeColors.darkGrey}"
        class="artifact-border"
      />
      <circle 
        cx="100" cy="100" r="${radius - ARTIFACT_BORDER_WIDTH}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
        class="artifact-svg"
      />
    `
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
    { width: outerWidth + xOffset, height: outerHeight, marginTop: 6 },
    { x: 30, y: 20, width: 180, height: 100, truncateLength: 90 },
    `
      <polygon 
        points="
          ${xOffset},0 
          ${outerWidth + xOffset},0 
          ${outerWidth},${outerHeight} 
          0,${outerHeight}"
        fill="${ThemeColors.darkGrey}"
        class="artifact-border"
      />
      <polygon
        points="
          ${xOffset + ARTIFACT_BORDER_WIDTH},${ARTIFACT_BORDER_WIDTH}
          ${
            outerWidth + xOffset - ARTIFACT_BORDER_WIDTH
          },${ARTIFACT_BORDER_WIDTH}
          ${outerWidth - ARTIFACT_BORDER_WIDTH},${
      outerHeight - ARTIFACT_BORDER_WIDTH
    } 
          ${ARTIFACT_BORDER_WIDTH},${outerHeight - ARTIFACT_BORDER_WIDTH}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
        class="artifact-svg"
      />
    `
  );
}

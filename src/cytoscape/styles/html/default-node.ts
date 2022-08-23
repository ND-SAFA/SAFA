import { ArtifactData } from "@/types";
import { getBackgroundColor, ThemeColors } from "@/util";
import { ARTIFACT_BORDER_WIDTH } from "@/cytoscape";
import { svgNode } from "./core-svg";

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

import { TimNodeData } from "@/types";
import { ThemeColors } from "@/util";
import {
  ARTIFACT_BORDER_WIDTH,
  TIM_NODE_HEIGHT,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config";
import { svgDetails, svgDiv, svgTitle } from "./core-svg";

/**
 * Creates the SVG TIM node.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
export function svgTIM(data: TimNodeData): string {
  const x = 10;
  const y = 30;
  const color = ThemeColors.darkGrey;

  return `
    <svg
      width="${TIM_NODE_WIDTH}" height="${TIM_NODE_HEIGHT}"
      class="artifact-svg-wrapper"
      style="margin-top: 7px"
    >
      <rect 
        rx="8" width="${TIM_NODE_WIDTH}" height="${TIM_NODE_HEIGHT}"
        fill="${color}"
        class="artifact-border"
      />
      <rect
        x="${ARTIFACT_BORDER_WIDTH}" y="${ARTIFACT_BORDER_WIDTH}" rx="7" 
        width="${TIM_NODE_WIDTH - ARTIFACT_BORDER_WIDTH * 2}" 
        height="${TIM_NODE_HEIGHT - ARTIFACT_BORDER_WIDTH * 2}"
        fill="${ThemeColors.lightGrey}"
        class="artifact-svg"
      />
      ${svgTitle(data.id, y)}
      ${svgDiv({ x, y: y + 17, width: TIM_NODE_WIDTH - x * 2, color })}
      ${svgDetails(`${data.count} Nodes`, y + 47)}
    </svg>
    `;
}

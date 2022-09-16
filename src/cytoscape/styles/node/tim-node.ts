import { TimNodeData } from "@/types";
import { ThemeColors } from "@/util";
import { TIM_NODE_HEIGHT, TIM_NODE_WIDTH } from "@/cytoscape/styles/config";
import { svgRect } from "./node-shapes";
import { svgDiv, svgTitle } from "./svg-node";

/**
 * Creates the SVG TIM node.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
export function svgTIM(data: TimNodeData): string {
  const x = 10;
  const y = 10;
  const color = ThemeColors.darkGrey;

  return `
    <svg
      width="${TIM_NODE_WIDTH}" height="${TIM_NODE_HEIGHT}"
      class="artifact-svg-wrapper"
      style="margin-top: 7px"
    >
      ${svgRect(
        {
          width: TIM_NODE_WIDTH,
          height: TIM_NODE_HEIGHT,
        },
        color,
        ThemeColors.lightGrey,
        8
      )}
      ${svgTitle(data.id, y, "type")}
      ${svgDiv({ x, y: y + 37, width: TIM_NODE_WIDTH - x * 2, color })}
      ${svgTitle(`${data.count} Nodes`, y + 50, "count")}
    </svg>
  `;
}

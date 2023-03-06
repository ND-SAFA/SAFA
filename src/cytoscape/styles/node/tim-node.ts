import { TimNodeCytoElementData } from "@/types";
import { getBackgroundColor, getBorderColor } from "@/util";
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
export function svgTIM(data: TimNodeCytoElementData): string {
  const x = 10;
  const y = 10;
  const borderColor = getBorderColor();
  const bgColor = getBackgroundColor("", data.dark);
  const count = data.count == 1 ? "1 Artifact" : `${data.count} Artifacts`;

  return `
    <svg
      width="${TIM_NODE_WIDTH}" height="${TIM_NODE_HEIGHT}"
      class="artifact-svg-wrapper"
      style="margin-top: 7px"
      data-cy="tim-node"
      data-cy-name="${data.artifactType}"
    >
      ${svgRect(
        {
          width: TIM_NODE_WIDTH,
          height: TIM_NODE_HEIGHT,
        },
        borderColor,
        bgColor,
        8
      )}
      ${svgTitle(data.artifactType, y, "type")}
      ${svgDiv({
        x,
        y: y + 37,
        width: TIM_NODE_WIDTH - x * 2,
        color: borderColor,
      })}
      ${svgTitle(count, y + 50, "count")}
    </svg>
  `;
}

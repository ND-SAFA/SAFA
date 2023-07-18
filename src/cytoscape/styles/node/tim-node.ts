import { TimNodeCytoElementData } from "@/types";
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
  const x = 20;
  const y = 25;
  const count = data.count == 1 ? "1 Artifact" : `${data.count} Artifacts`;

  return `
    <svg
      width="${TIM_NODE_WIDTH}" height="${TIM_NODE_HEIGHT}"
      class="artifact-svg-wrapper tim-svg-wrapper"
      data-cy="tim-node"
      data-cy-name="${data.artifactType}"
    >
      ${svgRect(
        {
          width: TIM_NODE_WIDTH,
          height: TIM_NODE_HEIGHT,
          color: data.typeColor,
        },
        8
      )}
      ${svgTitle(data.artifactType, y, "type")}
      ${svgDiv({
        x,
        y: y + 48,
        width: TIM_NODE_WIDTH - x * 2,
        color: data.typeColor,
      })}
      ${svgTitle(count, y + 70, "count")}
    </svg>
  `;
}

import { ArtifactData, SvgStyle } from "@/types";
import { ThemeColors } from "@/util";
import { ARTIFACT_BORDER_WIDTH, ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape";
import { getWarnings } from "./artifact-helper";
import { svgStoplight } from "./artifact-stoplight";

/**
 * Creates the SVG for representing a safety case node's footer.
 *
 * @param data - The artifact data to render.
 * @param outerStyle - The outer style of the node.
 *
 * @return stringified SVG for the node.
 */
export function svgFooter(
  data: ArtifactData,
  outerStyle: Pick<SvgStyle, "width" | "height">
): string {
  const baseY = outerStyle.height + 4;
  const textY = data.childDeltaStates?.length
    ? outerStyle.height + 20
    : outerStyle.height + 26;
  const iconY = textY - 16;
  const warningCount = getWarnings(data);
  const hasWarnings = warningCount > 0;
  const hasChildren = (data.hiddenChildren || 0) > 0;

  if (!hasChildren && !hasWarnings && data.childDeltaStates?.length === 0) {
    return "";
  }

  const children = hasChildren
    ? `
      <text 
        y="${textY}"
        x="${hasWarnings ? 20 : 80}"
        fill="${ThemeColors.black}"
      >
        ${data.hiddenChildren} Hidden
      </text>
      <foreignObject 
        x="${hasWarnings ? 5 : 62}"
        y="${iconY}" 
        width="20" height="20"
      >
        <div style="font-family: Material Icons;">expand_more</div>
      </foreignObject>
    `
    : "";

  const warnings =
    warningCount > 0
      ? `
        <text 
          x="${hasChildren ? outerStyle.width - 80 : 80}"
          y="${textY}" 
          fill="${ThemeColors.black}"
        >
          ${warningCount} Warning${warningCount !== 1 ? "s" : ""}
        </text>
        <foreignObject 
          x="${hasChildren ? outerStyle.width - 100 : 62}" 
          y="${iconY - 1}" 
          width="20" height="20"
        >
          <div style="font-family: Material Icons; color: ${
            ThemeColors.warning
          }">
            warning
          </div>
        </foreignObject>
      `
      : "";

  return `
    <rect 
      x="0" 
      y="${baseY}" 
      rx="8" 
      width="${outerStyle.width}" 
      height="${ARTIFACT_CHILDREN_HEIGHT}"
      fill="${ThemeColors.darkGrey}"
      class="artifact-border"
    />
    <rect
      x="${ARTIFACT_BORDER_WIDTH}" 
      y="${baseY + ARTIFACT_BORDER_WIDTH}"
      rx="7" 
      width="${outerStyle.width - ARTIFACT_BORDER_WIDTH * 2}" 
      height="${ARTIFACT_CHILDREN_HEIGHT - ARTIFACT_BORDER_WIDTH * 2}"
      fill="${ThemeColors.lightGrey}"
      class="artifact-svg"
    />
    ${children}
    ${warnings}
    ${svgStoplight(data, {
      x: 6,
      y: textY + 4,
      width: outerStyle.width - 12,
    })}
  `;
}

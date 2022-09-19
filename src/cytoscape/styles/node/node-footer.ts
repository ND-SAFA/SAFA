import { ArtifactData, SvgStyle } from "@/types";
import { ThemeColors } from "@/util";
import { ARTIFACT_BORDER_WIDTH, ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape";
import { svgStoplight } from "./node-stoplight";
import { getWarnings } from "./node-helper";

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
  const warningCount = getWarnings(data);
  const hasWarnings = warningCount > 0;
  const hasChildren = (data.hiddenChildren || 0) > 0;

  if (!hasChildren && !hasWarnings && data.childDeltaStates?.length === 0) {
    return "";
  }

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
    ${svgChildren(data.hiddenChildren || 0, hasWarnings, textY)}
    ${svgWarnings(warningCount, hasChildren, textY, outerStyle.width)}
    ${svgStoplight(data, {
      x: 6,
      y: textY + 4,
      width: outerStyle.width - 12,
    })}
  `;
}

/**
 * Renders the number of hidden children below a node.
 *
 * @param hiddenChildren - The number of hidden children.
 * @param hasWarnings - Whether warnings are also rendered.
 * @param textY - The yPosition to render text at.
 *
 * @return stringified SVG for the node.
 */
function svgChildren(
  hiddenChildren: number,
  hasWarnings: boolean,
  textY: number
): string {
  const iconY = textY - 16;

  if (hiddenChildren === 0) return "";

  return `
        <text 
          y="${textY}"
          x="${hasWarnings ? 20 : 80}"
          fill="${ThemeColors.black}"
        >
          ${hiddenChildren} Hidden
        </text>
        <foreignObject 
          x="${hasWarnings ? 5 : 62}"
          y="${iconY}" 
          width="20" height="20"
        >
          <div style="font-family: Material Icons;">expand_more</div>
        </foreignObject>
  `;
}

/**
 * Renders the number of warnings on a node.
 *
 * @param warningCount - The number of warnings.
 * @param hasChildren - Whether children are also rendered.
 * @param textY - The yPosition to render text at.
 * @param width - The outer width of the footer area.
 *
 * @return stringified SVG for the node.
 */
function svgWarnings(
  warningCount: number,
  hasChildren: boolean,
  textY: number,
  width: number
): string {
  const iconY = textY - 17;

  if (warningCount === 0) return "";

  return `
        <text 
          x="${hasChildren ? width - 80 : 80}"
          y="${textY}" 
          fill="${ThemeColors.black}"
        >
          ${warningCount} Warning${warningCount !== 1 ? "s" : ""}
        </text>
        <foreignObject 
          x="${hasChildren ? width - 100 : 62}" 
          y="${iconY - 1}" 
          width="20" height="20"
        >
          <div 
            style="font-family: Material Icons; 
                   color: ${ThemeColors.warningDark}"
          >
            warning
          </div>
        </foreignObject>
  `;
}

import { ArtifactCytoElementData, SvgStyle } from "@/types";
import { getBackgroundColor, getBorderColor, ThemeColors } from "@/util";
import { ARTIFACT_BORDER_WIDTH, ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape";
import { svgIcon, svgText } from "./svg-text";
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
  data: ArtifactCytoElementData,
  outerStyle: Pick<SvgStyle, "width" | "height">
): string {
  const baseY = outerStyle.height + 4;
  const textY = data.childDeltaStates?.length
    ? outerStyle.height + 2
    : outerStyle.height + 8;
  const warningCount = getWarnings(data);
  const hasWarnings = warningCount > 0;
  const hasChildren = (data.hiddenChildren || 0) > 0;
  const backgroundColor =
    hasWarnings && !data.dark
      ? ThemeColors.warningLight
      : getBackgroundColor(data.artifactDeltaState, data.dark);
  const borderColor = hasWarnings
    ? ThemeColors.warningDark
    : getBorderColor(data.artifactDeltaState);

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
      fill="${borderColor}"
      class="artifact-border"
    />
    <rect
      x="${ARTIFACT_BORDER_WIDTH}" 
      y="${baseY + ARTIFACT_BORDER_WIDTH}"
      rx="7" 
      width="${outerStyle.width - ARTIFACT_BORDER_WIDTH * 2}" 
      height="${ARTIFACT_CHILDREN_HEIGHT - ARTIFACT_BORDER_WIDTH * 2}"
      fill="${backgroundColor}"
      class="artifact-svg"
    />
    ${svgChildren(data.hiddenChildren || 0, hasWarnings, textY)}
    ${svgWarnings(warningCount, hasChildren, textY, outerStyle.width)}
    ${svgStoplight(data, {
      x: 6,
      y: textY + 22,
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
  if (hiddenChildren === 0) return "";

  const style = {
    y: textY,
    x: hasWarnings ? 5 : 62,
    width: 120,
    height: 30,
  };

  return (
    svgIcon(
      {
        ...style,
        y: style.y - 2,
      },
      "expand_more"
    ) +
    svgText(
      `${hiddenChildren} Hidden`,
      {
        ...style,
        x: style.x + 20,
      },
      "children"
    )
  );
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
  if (warningCount === 0) return "";

  const style = {
    x: hasChildren ? width - 106 : 60,
    y: textY,
    width: 120,
    height: 30,
  };

  return (
    svgIcon(
      {
        ...style,
        y: style.y - 2,
      },
      "warning",
      ThemeColors.warningDark
    ) +
    svgText(
      `${warningCount} Warning${warningCount !== 1 ? "s" : ""}`,
      {
        ...style,
        x: style.x + 22,
      },
      "warnings"
    )
  );
}

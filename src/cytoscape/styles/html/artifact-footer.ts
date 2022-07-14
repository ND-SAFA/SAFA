import { ArtifactData, SvgStyle } from "@/types";
import { ThemeColors } from "@/util";
import { svgStoplight } from "./artifact-stoplight";
import { getWarnings } from "./artifact-helper";
import { ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape/styles/config";

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
        fill="${ThemeColors.artifactText}"
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
          fill="${ThemeColors.artifactText}"
        >
          ${warningCount} Warning${warningCount !== 1 ? "s" : ""}
        </text>
        <foreignObject 
          x="${hasChildren ? outerStyle.width - 100 : 62}" 
          y="${iconY - 1}" 
          width="20" height="20"
        >
          <div style="font-family: Material Icons; color: ${
            ThemeColors.artifactWarning
          }">
            warning
          </div>
        </foreignObject>
      `
      : "";

  return `
    <rect 
      x="0" y="${outerStyle.height + 4}" rx="8" 
      width="${outerStyle.width}" height="${ARTIFACT_CHILDREN_HEIGHT}"
      fill="${ThemeColors.artifactBorder}"
    />
    <rect
      x="1" y="${outerStyle.height + 5}" rx="7" 
      width="${outerStyle.width - 2}" height="${ARTIFACT_CHILDREN_HEIGHT - 2}"
      fill="${ThemeColors.artifactDefault}"
    />
    ${children}
    ${warnings}
    ${svgStoplight(data, {
      x: 4,
      y: textY + 6,
      width: outerStyle.width - 8,
    })}
  `;
}

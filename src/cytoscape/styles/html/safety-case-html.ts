import { ArtifactData, SvgStyle } from "@/types";
import { capitalize, getBackgroundColor, ThemeColors } from "@/util";
import { svgStoplight } from "./artifact-stoplight";
import { getBody, getWarnings } from "./artifact-helper";

/**
 * Creates the HTML for representing a safety case node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
export function htmlSafetyCase(data: ArtifactData): string {
  switch (data.safetyCaseType) {
    case "GOAL":
      return svgGoal(data);
    case "CONTEXT":
      return svgContext(data);
    case "SOLUTION":
      return svgSolution(data);
    case "STRATEGY":
      return svgStrategy(data);
    default:
      return "";
  }
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
    { width: outerWidth, height: outerHeight, marginTop: 6 },
    { x: 10, y: 20, width: 180, height: 100, truncateLength: 90 },
    `
      <rect 
        width="${outerWidth}" height="${outerHeight}"
        fill="${ThemeColors.artifactBorder}"
      />
      <rect
        x="1" y="1" width="${outerWidth - 2}" height="${outerHeight - 2}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
      />
    `
  );
}

/**
 * Creates the SVG safety case context.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgContext(data: ArtifactData): string {
  const outerHeight = 160;
  const outerWidth = 206;

  return svgNode(
    data,
    { width: outerWidth, height: outerHeight, marginTop: 6 },
    { x: 10, y: 20, width: 180, height: 100, truncateLength: 90 },
    `
      <rect 
        rx="8" width="${outerWidth}" height="${outerHeight}"
        fill="${ThemeColors.artifactBorder}"
      />
      <rect
        x="1" y="1" rx="7" width="${outerWidth - 2}" height="${outerHeight - 2}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
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
  return svgNode(
    data,
    { width: 200, height: 200, marginTop: 7 },
    {
      x: 40,
      y: 35,
      width: 120,
      height: 70,
      bodyWidth: 160,
      truncateLength: 65,
    },
    `
      <circle 
        cx="100" cy="100" r="92"
        fill="${ThemeColors.artifactBorder}"
      />
      <circle 
        cx="100" cy="100" r="91"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
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
        fill="${ThemeColors.artifactBorder}"
      />
      <polygon
        points="
          ${xOffset + 1},1 
          ${outerWidth + xOffset - 1},1 
          ${outerWidth - 1},${outerHeight - 1} 
          1,${outerHeight - 1}"
        fill="${getBackgroundColor(data.artifactDeltaState)}"
      />
    `
  );
}

/**
 * Creates the SVG safety case node.
 *
 * @param data - The artifact data to render.
 * @param outerStyle - The styles to render the SVG with.
 * @param innerStyle - The styles to render the inner content with.
 * @param svgShape - The SVG for rendering the node's shape.
 *
 * @return stringified SVG for the node.
 */
function svgNode(
  data: ArtifactData,
  outerStyle: Pick<SvgStyle, "width" | "height"> & { marginTop: number },
  innerStyle: SvgStyle & { truncateLength: number; bodyWidth?: number },
  svgShape: string
): string {
  const { x, y, width, height, truncateLength, bodyWidth } = innerStyle;

  return `
    <div>
      <svg 
        width="${outerStyle.width}" height="${outerStyle.height}" 
        style="margin-top: ${outerStyle.marginTop}px"
      >
        ${svgShape}
        ${svgTitle(capitalize(data.safetyCaseType || ""), y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgStoplight(data, { x, y: y + 9, width })}
        ${svgDetails(data, y + 27)}
        ${svgBody(data, {
          x,
          y: y + 30,
          width: bodyWidth || width,
          height,
          truncateLength,
        })}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG for representing a safety case node's title.
 *
 * @param title - The title of the node.
 * @param yPos - The y position to start drawing at.
 *
 * @return stringified SVG for the node.
 */
function svgTitle(title: string, yPos: number): string {
  return `
   <text 
      x="50%" y="${yPos}" text-anchor="middle"
      fill="${ThemeColors.artifactText}" 
    >
      ${title}
    </text>
  `;
}

/**
 * Creates the SVG for representing a safety case node's divider.
 *
 * @param style - The position style to draw with.
 *
 * @return stringified SVG for the node.
 */
function svgDiv(style: Omit<SvgStyle, "height">): string {
  return `
     <line 
        x1="${style.x}" y1="${style.y}" 
        x2="${style.x + style.width}" y2="${style.y}" 
        stroke="rgb(136, 136, 136)" 
        shape-rendering="crispEdges"
      />
  `;
}

/**
 * Creates the SVG for representing a safety case node's warnings and collapsed children.
 *
 * @param data - The artifact data to render.
 * @param yPos - The y position to start drawing at.
 *
 * @return stringified SVG for the node.
 */
function svgDetails(data: ArtifactData, yPos: number): string {
  const warningCount = getWarnings(data);
  const children = data.hiddenChildren
    ? `
      <tspan fill="${ThemeColors.artifactBorder}">
        ${data.hiddenChildren}H
      </tspan>
    `
    : "";
  const warnings =
    warningCount > 0
      ? `
        <tspan fill="${ThemeColors.artifactWarning}">
          ${warningCount}!
        </tspan>
      `
      : "";

  return `
    <text x="50%" y="${yPos}" text-anchor="middle" shape-rendering="crispEdges">
      <tspan fill="${ThemeColors.artifactText}">${data.artifactName}</tspan>
      ${children}${warnings}
    </text>
  `;
}

/**
 * Creates the SVG for representing a safety case node's body.
 *
 * @param data - The artifact data to render.
 * @param style - The position style to draw with.
 *
 * @return stringified SVG for the node.
 */
function svgBody(
  data: ArtifactData,
  style: SvgStyle & { truncateLength: number }
): string {
  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" height="${style.height}"
    >
      <span class="text-body-2">
        ${getBody(data.body, style.truncateLength)}
      </span>
    </foreignObject>
  `;
}

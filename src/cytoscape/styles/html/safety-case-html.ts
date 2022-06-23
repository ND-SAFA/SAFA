import { ArtifactData, SvgStyle } from "@/types";
import { getBackgroundColor, ThemeColors } from "@/util";
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
  const color = getBackgroundColor(data.artifactDeltaState);
  const x = 10;
  const y = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const width = 180;

  return `
    <div>
      <svg 
        width="${outerWidth}" height="${outerHeight}" 
        style="margin-top: 6px"
      >
        <rect 
          width="${outerWidth}" height="${outerHeight}"
          fill="${ThemeColors.artifactBorder}"
        />
        <rect
          x="1" y="1" fill="${color}"
          width="${outerWidth - 2}" height="${outerHeight - 2}"
        />
        ${svgTitle("Goal", y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgStoplight(data, { x, y: y + 9, width })}
        ${svgDetails(data, y + 27)}
        ${svgBody(data, 90, {
          x,
          y: y + 30,
          width,
          height: 100,
        })}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG safety case context.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgContext(data: ArtifactData): string {
  const color = getBackgroundColor(data.artifactDeltaState);
  const x = 10;
  const y = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const width = 180;

  return `
    <div>
      <svg 
        width="${outerWidth}" height="${outerHeight}" 
        style="margin-top: 6px"
      >
        <rect 
          rx="8" fill="${ThemeColors.artifactBorder}"
          width="${outerWidth}" height="${outerHeight}"
        />
        <rect
          x="1" y="1" rx="7" fill="${color}"
          width="${outerWidth - 2}" height="${outerHeight - 2}"
        />
        ${svgTitle("Context", y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgStoplight(data, { x, y: y + 9, width })}
        ${svgDetails(data, y + 27)}
        ${svgBody(data, 90, {
          x,
          y: y + 30,
          width,
          height: 100,
        })}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG safety case solution.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgSolution(data: ArtifactData): string {
  const color = getBackgroundColor(data.artifactDeltaState);
  const x = 40;
  const y = 35;
  const width = 120;

  return `
    <div>
      <svg 
        width="200" height="200" 
        style="margin-top: 7px"
      >
        <circle 
          cx="100" cy="100" r="92"
          fill="${ThemeColors.artifactBorder}"
        />
        <circle 
          cx="100" cy="100" r="91"
          fill="${color}"
        />
        ${svgTitle("Solution", y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgStoplight(data, { x, y: y + 9, width })}
        ${svgDetails(data, y + 25)}
        ${svgBody(data, 65, {
          x,
          y: y + 30,
          width: 160,
          height: 70,
        })}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG safety case strategy.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified SVG for the node.
 */
function svgStrategy(data: ArtifactData): string {
  const color = getBackgroundColor(data.artifactDeltaState);
  const x = 30;
  const y = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const width = 180;
  const xOffset = 20;

  return `
    <div>
      <svg 
        width="${outerWidth + xOffset}" height="${outerHeight}" 
        style="margin-top: 6px"
      >
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
          fill="${color}"
        />
        ${svgTitle("Strategy", y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgStoplight(data, { x, y: y + 9, width })}
        ${svgDetails(data, y + 27)}
        ${svgBody(data, 90, {
          x,
          y: y + 30,
          width,
          height: 100,
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
 * @param truncateLength - The number of characters to print before truncating.
 * @param style - The position style to draw with.
 *
 * @return stringified SVG for the node.
 */
function svgBody(
  data: ArtifactData,
  truncateLength: number,
  style: SvgStyle
): string {
  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" height="${style.height}"
    >
      <span class="text-body-2">${getBody(data.body, truncateLength)}</span>
    </foreignObject>
  `;
}

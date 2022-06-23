import { ArtifactData, ArtifactDeltaState } from "@/types";
import { getBackgroundColor, ThemeColors } from "@/util";

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
  const xPos = 10;
  const yPos = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const innerWidth = 180;

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
          x="1" y="1" 
          width="${outerWidth - 2}" height="${outerHeight - 2}"
          fill="${color}"
        />
        ${svgTitle("Goal", yPos)}
        ${svgDiv(xPos, yPos + 7, innerWidth)}
        ${svgStoplight(data, xPos, yPos + 9, innerWidth)}
        ${svgDetails(data, yPos + 27)}
        ${svgBody(data, xPos, yPos + 30, innerWidth, 100, 90)}
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
  const xPos = 10;
  const yPos = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const innerWidth = 180;

  return `
    <div>
      <svg 
        width="${outerWidth}" height="${outerHeight}" 
        style="margin-top: 6px"
      >
        <rect 
          rx="8" 
          width="${outerWidth}" height="${outerHeight}"
          fill="${ThemeColors.artifactBorder}"
        />
        <rect
          x="1" y="1" rx="7"
          width="${outerWidth - 2}" height="${outerHeight - 2}"
          fill="${color}"
        />
        ${svgTitle("Context", yPos)}
        ${svgDiv(xPos, yPos + 7, innerWidth)}
        ${svgStoplight(data, xPos, yPos + 9, innerWidth)}
        ${svgDetails(data, yPos + 27)}
        ${svgBody(data, xPos, yPos + 30, innerWidth, 100, 90)}
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
  const xPos = 40;
  const yPos = 35;
  const divWidth = 120;

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
        ${svgTitle("Solution", yPos)}
        ${svgDiv(xPos, yPos + 7, divWidth)}
        ${svgStoplight(data, xPos, yPos + 9, divWidth)}
        ${svgDetails(data, yPos + 25)}
        ${svgBody(data, 20, yPos + 30, 160, 70, 65)}
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
  const xPos = 30;
  const yPos = 20;
  const outerHeight = 160;
  const outerWidth = 206;
  const innerWidth = 180;
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
        ${svgTitle("Strategy", yPos)}
        ${svgDiv(xPos, yPos + 7, innerWidth)}
        ${svgStoplight(data, xPos, yPos + 9, innerWidth)}
        ${svgDetails(data, yPos + 27)}
        ${svgBody(data, xPos, yPos + 30, innerWidth, 100, 90)}
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
 * @param xPos - The x position to start drawing at.
 * @param yPos - The y position to start drawing at.
 * @param width - The width of the divider.
 *
 * @return stringified SVG for the node.
 */
function svgDiv(xPos: number, yPos: number, width: number): string {
  return `
     <line 
        x1="${xPos}" y1="${yPos}" 
        x2="${xPos + width}" y2="${yPos}" 
        stroke="rgb(136, 136, 136)" 
        shape-rendering="crispEdges"
      />
  `;
}

/**
 * Creates the SVG for representing a safety case node's child delta states.
 *
 * @param data - The artifact data to render.
 * @param xPos - The x position to start drawing at.
 * @param yPos - The y position to start drawing at.
 * @param width - The width of the stoplight to draw.
 *
 * @return stringified SVG for the node.
 */
function svgStoplight(
  data: ArtifactData,
  xPos: number,
  yPos: number,
  width: number
): string {
  const { childDeltaStates = [] } = data;
  let stoplight = "";
  let currentPos = xPos;

  const toRender = [
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.ADDED),
      color: ThemeColors.artifactAdded,
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.MODIFIED),
      color: ThemeColors.artifactModified,
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.REMOVED),
      color: ThemeColors.artifactRemoved,
    },
  ];

  const count = toRender.filter(({ doRender }) => doRender).length;
  const incrementWidth = width / count;

  for (const { doRender, color } of toRender) {
    if (!doRender) continue;

    stoplight += `
        <line 
          x1="${currentPos}" y1="${yPos}" 
          x2="${currentPos + incrementWidth}" y2="${yPos}" 
          stroke="${color}" 
          stroke-width="4"
          shape-rendering="crispEdges"
        />
    `;
    currentPos += incrementWidth;
  }

  return stoplight;
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
  const warningCount = data.hiddenChildren
    ? (data.warnings?.length || 0) + (data.childWarnings?.length || 0)
    : data.warnings?.length || 0;
  let details = "";

  if (data.hiddenChildren) {
    details += `
      <tspan fill="${ThemeColors.artifactBorder}">
        ${data.hiddenChildren}H
      </tspan>
    `;
  }

  if (warningCount > 0) {
    details += `
      <tspan fill="${ThemeColors.artifactWarning}">
        ${warningCount}!
      </tspan>
    `;
  }

  return `
    <text x="50%" y="${yPos}" text-anchor="middle" shape-rendering="crispEdges">
      <tspan fill="${ThemeColors.artifactText}">
        ${data.artifactName}
      </tspan>
      ${details}
    </text>
  `;
}

/**
 * Creates the SVG for representing a safety case node's body.
 *
 * @param data - The artifact data to render.
 * @param xPos - The x position to start drawing at.
 * @param yPos - The y position to start drawing at.
 * @param width - The width of the text area.
 * @param height - The height of the text area.
 * @param truncateLength - The number of characters to print before truncating.
 *
 * @return stringified SVG for the node.
 */
function svgBody(
  data: ArtifactData,
  xPos: number,
  yPos: number,
  width: number,
  height: number,
  truncateLength: number
): string {
  const body =
    data.body.length > truncateLength
      ? data.body.slice(0, truncateLength) + "..."
      : data.body;

  return `
    <foreignObject x="${xPos}" y="${yPos}" width="${width}" height="${height}">
      <span class="text-body-2">
        ${body}
      </span>
    </foreignObject>
  `;
}

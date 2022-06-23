import { ArtifactData, ArtifactDeltaState } from "@/types";
import { ThemeColors } from "@/util";

/**
 * Creates the HTML for representing a safety case node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
export function _htmlSafetyCase(data: ArtifactData): string {
  //TODO: remove testing
  data.childDeltaStates = [
    ArtifactDeltaState.ADDED,
    ArtifactDeltaState.MODIFIED,
    ArtifactDeltaState.REMOVED,
  ];
  data.warnings = [{ ruleMessage: "Warn", ruleName: "Warn" }];
  data.hiddenChildren = 3;
  data.body = "So many words omg woo! ".repeat(10);

  switch (data.safetyCaseType) {
    case "GOAL":
      return "";
    case "CONTEXT":
      return "";
    case "SOLUTION":
      return htmlSafetyCaseSolution(data);
    case "STRATEGY":
      return "";
    default:
      return "";
  }
}

/**
 * Creates the HTML safety case solution.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCaseSolution(data: ArtifactData): string {
  return `
    <div>
      <svg 
        width="200" 
        height="200" 
        style="margin-top: 7px"
      >
        <circle 
          cx="100" cy="100" r="92"
          fill="${ThemeColors.artifactBorder}"
        />
        <circle 
          cx="100" cy="100" r="91"
          fill="${ThemeColors.artifactDefault}"
        />
        <text 
          x="72" y="35" 
          fill="${ThemeColors.artifactText}" 
        >
          Solution
        </text>
        ${svgDiv(40, 42, 120)}
        ${svgStoplight(data, 40, 44, 120)}
        ${svgDetails(data, 30, 60)}
        ${svgBody(data, 20, 65, 160, 70, 65)}
      </svg>
    </div>
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

  let stoplight = "";
  let currentPos = xPos;

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
 * @param xPos - The x position to start drawing at.
 * @param yPos - The y position to start drawing at.
 *
 * @return stringified SVG for the node.
 */
function svgDetails(data: ArtifactData, xPos: number, yPos: number): string {
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
    <text x="${xPos}" y="${yPos}">
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

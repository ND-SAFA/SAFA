import {
  ArtifactData,
  ArtifactDeltaState,
  NodeChildDelta,
  SvgStyle,
} from "@/types";
import { ThemeColors } from "@/util";

/**
 * Creates the HTML for representing an artifact node's child delta states.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
export function htmlStoplight(data: ArtifactData): string {
  const childDeltaStates = getChildDeltaStates(data);

  if (childDeltaStates.length === 0) {
    return "";
  }

  return `
    <div class="d-flex artifact-stoplight">
      ${childDeltaStates.map(({ node }) => node).join("")}
    </div>
  `;
}

/**
 * Creates the SVG for representing a safety case node's child delta states.
 *
 * @param data - The artifact data to render.
 * @param style - The position style to draw with.
 *
 * @return stringified SVG for the node.
 */
export function svgStoplight(
  data: ArtifactData,
  style: Omit<SvgStyle, "height">
): string {
  const childDeltaStates = getChildDeltaStates(data);
  const incrementWidth = style.width / childDeltaStates.length;
  let stoplight = "";
  let currentPos = style.x;

  for (const { color } of childDeltaStates) {
    stoplight += `
        <line 
          x1="${currentPos}" y1="${style.y}" 
          x2="${currentPos + incrementWidth}" y2="${style.y}" 
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
 * Returns all child delta states that should be rendered.
 *
 * @param data - The artifact data to render.
 *
 * @return The child delta states to render.
 */
function getChildDeltaStates(data: ArtifactData): NodeChildDelta[] {
  const { childDeltaStates = [] } = data;

  const toRender = [
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.ADDED),
      color: ThemeColors.artifactAdded,
      node: "<div class='artifact-added flex-grow-1'></div>",
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.MODIFIED),
      color: ThemeColors.artifactModified,
      node: "<div class='artifact-modified flex-grow-1'></div>",
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.REMOVED),
      color: ThemeColors.artifactRemoved,
      node: "<div class='artifact-removed flex-grow-1'></div>",
    },
  ];

  return toRender.filter(({ doRender }) => doRender);
}

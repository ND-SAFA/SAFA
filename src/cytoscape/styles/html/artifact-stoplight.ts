import {
  ArtifactData,
  ArtifactDeltaState,
  NodeChildDelta,
  SvgStyle,
} from "@/types";
import { ThemeColors } from "@/util";

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
  const incrementWidth = style.width / childDeltaStates.length - 1;
  let stoplight = "";
  let currentPos = style.x;

  for (const { color } of childDeltaStates) {
    stoplight += `
        <rect
          x="${currentPos}" y="${style.y}" rx="5" 
          width="${incrementWidth}" height="10"
          fill="${color}"
        />
    `;
    currentPos += incrementWidth + 1;
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
      color: ThemeColors.added,
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.MODIFIED),
      color: ThemeColors.modified,
    },
    {
      doRender: childDeltaStates.includes(ArtifactDeltaState.REMOVED),
      color: ThemeColors.removed,
    },
  ];

  return toRender.filter(({ doRender }) => doRender);
}

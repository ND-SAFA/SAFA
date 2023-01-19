import {
  ArtifactCytoElementData,
  ReservedArtifactType,
  SvgNodeStyle,
  SvgStyle,
} from "@/types";
import { capitalize, getBorderColor } from "@/util";
import { ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape/styles/config";
import { svgText } from "@/cytoscape/styles/node/svg-text";
import { svgFooter } from "./node-footer";
import { getBody, sanitizeText } from "./node-helper";

/**
 * Creates the SVG standard node.
 *
 * @param data - The artifact data to render.
 * @param style - The styles to render the SVG with.
 * @param svgShape - The SVG for rendering the node's shape.
 *
 * @return stringified SVG for the node.
 */
export function svgNode(
  data: ArtifactCytoElementData,
  style: SvgNodeStyle,
  svgShape: string
): string {
  const { outer, inner, marginTop, truncateLength, bodyWidth } = style;
  const { x, y, width, height } = inner;
  const deltaClass = `artifact-svg-delta-${data.artifactDeltaState}`;
  const title = data.safetyCaseType
    ? capitalize(data.safetyCaseType)
    : data.artifactType;
  const color = getBorderColor(data.artifactDeltaState);
  const footer = svgFooter(data, outer);
  const heightOffset = footer ? ARTIFACT_CHILDREN_HEIGHT + 6 : 6;
  const outerHeight = outer.height + heightOffset;
  const margin = `${marginTop + heightOffset}px`;
  const dataCy = data.isSelected ? "tree-node-selected" : "tree-node";

  return `
    <div>
      <svg 
        width="${outer.width}" 
        height="${outerHeight}" 
        style="margin-top: ${margin}; opacity: ${data.opacity};"
        class="artifact-svg-wrapper ${deltaClass}"
        data-cy="${dataCy}"
        data-cy-name="${sanitizeText(data.artifactName)}"
      >
        ${svgShape}
        ${svgTitle(title, y - 18, "type")}
        ${svgDiv({
          x,
          y: y + 7,
          width,
          color,
        })}
        ${svgTitle(data.artifactName, y + 10, "name")}
        ${svgBody(data, truncateLength, {
          x,
          y: y + 35,
          width: bodyWidth || width,
          height,
        })}
        ${footer}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG for representing a node's title.
 *
 * @param title - The title to render.
 * @param y - The y position to start drawing at.
 * @param dataCy - The data cy selector to append.
 *
 * @return stringified SVG for the node.
 */
export function svgTitle(title: string, y: number, dataCy: string): string {
  return svgText(
    title,
    {
      class: "align-center mx-2 text-ellipsis artifact-text",
      x: 0,
      y,
      width: "100%",
      height: 24,
    },
    dataCy
  );
}

/**
 * Creates the SVG for representing a node's divider.
 *
 * @param style - The style to draw with.
 *
 * @return stringified SVG for the node.
 */
export function svgDiv(style: Omit<SvgStyle, "height">): string {
  return `
     <line 
        x1="${style.x}" y1="${style.y}" 
        x2="${style.x + style.width}" y2="${style.y}" 
        stroke="${style.color}" 
        stroke-width="2"
        class="artifact-svg-div"
      />
  `;
}

/**
 * Creates the SVG for representing an node's body.
 *
 * @param data - The artifact to render.
 * @param truncateLength - The maximum characters of text to render.
 * @param style - The style to draw with.
 *
 * @return stringified SVG for the node.
 */
function svgBody(
  data: ArtifactCytoElementData,
  truncateLength: number,
  style: SvgStyle
): string {
  const code = data.artifactType === ReservedArtifactType.github;

  return svgText(
    getBody(data.body, truncateLength),
    { ...style, code },
    "body",
    `
      display: block;
      width: ${style.width}px;
      height: ${style.height}px;
      line-height: 1rem;
      text-align: ${code ? "left" : "center"};
    `
  );
}

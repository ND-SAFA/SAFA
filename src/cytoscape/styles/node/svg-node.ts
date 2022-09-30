import { ArtifactData, SvgNodeStyle, SvgStyle } from "@/types";
import { capitalize, getBorderColor } from "@/util";
import { ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape";
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
  data: ArtifactData,
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
        ${svgBody(data.body, truncateLength, {
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
 * @param yPos - The y position to start drawing at.
 * @param dataCy - The data cy selector to append.
 *
 * @return stringified SVG for the node.
 */
export function svgTitle(title: string, yPos: number, dataCy: string): string {
  return `
    <foreignObject y="${yPos}" height="24" width="100%">
      <span 
        class="text-body-1 align-center mx-2 text-ellipsis artifact-text" 
        data-cy="tree-node-${dataCy}"
      >
        ${sanitizeText(title)}
      </span >
    </foreignObject>
  `;
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
 * @param body - The body to render.
 * @param truncateLength - The maximum characters of text to render.
 * @param style - The style to draw with.
 *
 * @return stringified SVG for the node.
 */
function svgBody(
  body: string,
  truncateLength: number,
  style: SvgStyle
): string {
  const width = `${style.width}px`;
  const height = `${style.height}px`;

  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" 
      height="${style.height}"
    >
     <span
       class="text-body-1" 
       data-cy="tree-node-body"
       style="
         display: block;
         width: ${width};
         height: ${height};
         line-height: 1rem;
         text-align: center;
       "
     >
       ${getBody(body, truncateLength)}
     </span>
    </foreignObject>
  `;
}

import { ArtifactData, SvgStyle } from "@/types";
import { capitalize, getBorderColor } from "@/util";
import { ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape/styles/config";
import { svgFooter } from "./artifact-footer";
import { getBody } from "./artifact-helper";

/**
 * Creates the SVG standard node.
 *
 * @param data - The artifact data to render.
 * @param outerStyle - The styles to render the SVG with.
 * @param innerStyle - The styles to render the inner content with.
 * @param svgShape - The SVG for rendering the node's shape.
 *
 * @return stringified SVG for the node.
 */
export function svgNode(
  data: ArtifactData,
  outerStyle: Pick<SvgStyle, "width" | "height"> & { marginTop: number },
  innerStyle: SvgStyle & { truncateLength: number; bodyWidth?: number },
  svgShape: string
): string {
  const { x, y, width, height, truncateLength, bodyWidth } = innerStyle;
  const deltaClass = `artifact-svg-delta-${data.artifactDeltaState}`;
  const title = data.safetyCaseType
    ? capitalize(data.safetyCaseType)
    : capitalize(data.artifactType);
  const color = getBorderColor(data.artifactDeltaState);
  const footer = svgFooter(data, outerStyle);
  const heightOffset = footer ? ARTIFACT_CHILDREN_HEIGHT + 6 : 6;
  const dataCy = data.isSelected ? "tree-node-selected" : "tree-node";

  return `
    <div>
      <svg 
        width="${outerStyle.width}" 
        height="${outerStyle.height + heightOffset}" 
        style="
          margin-top: ${outerStyle.marginTop + heightOffset}px;
          opacity: ${data.opacity};
        "
        class="artifact-svg-wrapper ${deltaClass}"
        data-cy="${dataCy}"
        data-cy-name="${data.artifactName}"
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
        ${svgBody(data, {
          x,
          y: y + 35,
          width: bodyWidth || width,
          height,
          truncateLength,
        })}
        ${footer}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG for representing a safety case node's title.
 *
 * @param title - The title to render.
 * @param yPos - The y position to start drawing at.
 * @param dataCy - The data cy selector to append.
 *
 * @return stringified SVG for the node.
 */
export function svgTitle(title: string, yPos: number, dataCy = "name"): string {
  return `
    <foreignObject y="${yPos}" height="24" width="100%">
      <span 
        class="text-body-1 align-center mx-2 text-ellipsis artifact-text" 
        data-cy="tree-node-${dataCy}"
      >
        ${title}
      </span >
    </foreignObject>
  `;
}

/**
 * Creates the SVG for representing a safety case node's divider.
 *
 * @param style - The position style to draw with.
 *
 * @return stringified SVG for the node.
 */
export function svgDiv(
  style: Omit<SvgStyle, "height"> & { color: string }
): string {
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
      width="${style.width}" 
      height="${style.height}"
    >
     <span
       class="text-body-1" 
       data-cy="tree-node-body"
       style="
         display: block;
         width: ${style.width}px;
         height: ${style.height}px;
         line-height: 1rem;
         text-align: center;
       "
     >
       ${getBody(data.body, style.truncateLength)}
     </span>
    </foreignObject>
  `;
}

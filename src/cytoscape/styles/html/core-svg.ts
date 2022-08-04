import { ArtifactData, SvgStyle } from "@/types";
import { capitalize, getTextColor, ThemeColors } from "@/util";
import { getBody } from "./artifact-helper";
import { svgFooter } from "./artifact-footer";
import { ARTIFACT_CHILDREN_HEIGHT } from "@/cytoscape/styles/config";

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
export function svgNode(
  data: ArtifactData,
  outerStyle: Pick<SvgStyle, "width" | "height"> & { marginTop: number },
  innerStyle: SvgStyle & { truncateLength: number; bodyWidth?: number },
  svgShape: string
): string {
  const { x, y, width, height, truncateLength, bodyWidth } = innerStyle;
  const deltaClass = `artifact-svg-delta-${data.artifactDeltaState}`;

  return `
    <div style="opacity: ${data.opacity}">
      <svg 
        width="${outerStyle.width}" 
        height="${outerStyle.height + ARTIFACT_CHILDREN_HEIGHT + 6}" 
        style="margin-top: ${
          outerStyle.marginTop + ARTIFACT_CHILDREN_HEIGHT + 6
        }px"
        class="artifact-svg-wrapper ${deltaClass}"
      >
        ${svgShape}
        ${svgTitle(data, y)}
        ${svgDiv({ x, y: y + 7, width })}
        ${svgDetails(data, y + 27)}
        ${svgBody(data, {
          x,
          y: y + 35,
          width: bodyWidth || width,
          height,
          truncateLength,
        })}
        ${svgFooter(data, outerStyle)}
      </svg>
    </div>
  `;
}

/**
 * Creates the SVG for representing a safety case node's title.
 *
 * @param data - The artifact data to render.
 * @param yPos - The y position to start drawing at.
 *
 * @return stringified SVG for the node.
 */
function svgTitle(data: ArtifactData, yPos: number): string {
  const title = data.safetyCaseType
    ? capitalize(data.safetyCaseType)
    : capitalize(data.artifactType);

  return `
   <text 
      x="50%" y="${yPos}" text-anchor="middle"
      fill="${getTextColor(data.artifactDeltaState)}" 
      font-weight="600"
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
        stroke-width="2"
        class="artifact-svg-div"
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
  return `
    <text 
      x="50%" y="${yPos}" 
      text-anchor="middle" 
      shape-rendering="crispEdges"
      font-weight="600"
      fill="${getTextColor(data.artifactDeltaState)}"
    >
      ${data.artifactName}
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
      width="${style.width}" 
      height="${style.height}"
    >
     <span
       class="text-body-1" 
       style="
         display: block;
         width: ${style.width}px;
         height: ${style.height}px;
         line-height: 1rem;
         text-align: center;
         color: ${getTextColor(data.artifactDeltaState)}"
     >
       ${getBody(data.body, style.truncateLength)}
     </span>
    </foreignObject>
  `;
}

import { SvgStyle } from "@/types";
import { sanitizeText } from "./node-helper";

/**
 * Creates the SVG for representing text.
 *
 * @param text - The text to render.
 * @param style - The style to draw with.
 * @param dataCy - The data cy selector to append.
 * @param spanStyle - Any style to add to the span.
 *
 * @return stringified SVG for the node.
 */
export function svgText(
  text: string,
  style: { width: string | number } & Omit<SvgStyle, "width">,
  dataCy: string,
  spanStyle = ""
): string {
  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" 
      height="${style.height}"
    >
      <span
        class="text-body-1 ${style.class || ""}" 
        data-cy="tree-node-${dataCy}"
        style="${spanStyle}"
      >
        ${sanitizeText(text)}
      </span>
    </foreignObject>
  `;
}

/**
 * Creates the SVG for representing an icon.
 *
 * @param style - The style to draw with.
 * @param iconId - The icon to display.
 * @param color - The icon color to set.
 *
 * @return stringified SVG for the node.
 */
export function svgIcon(
  style: SvgStyle,
  iconId: string,
  color?: string
): string {
  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" 
      height="${style.height}"
    >
      <span style="
        font-family: Material Icons;  
        color: ${color};
        font-size: 20px;
      ">
        ${iconId}
      </span>
    </foreignObject>
  `;
}

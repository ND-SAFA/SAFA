import { SvgStyle } from "@/types";
import { sanitizeText } from "./node-helper";

/**
 * Creates the SVG for representing text.
 *
 * @param text - The text to render.
 * @param style - The style to draw with.
 * @param dataCy - The data cy selector to append.
 * @param spanStyle - Any style to add to the span.
 * @param icon - Any icon to prepend to the text.
 *
 * @return stringified SVG for the node.
 */
export function svgText(
  text: string,
  style: { width: string | number } & Omit<SvgStyle, "width">,
  dataCy: string,
  spanStyle = "",
  icon?: { id: string; color?: string }
): string {
  const htmlIcon = icon
    ? `
      <span style="
        font-family: Material Icons;  
        color: ${icon.color};
        font-size: 12px;
        font-weight: 600;
      ">
        ${icon.id}
      </span>
    `
    : "";

  return `
    <foreignObject 
      x="${style.x}" y="${style.y}" 
      width="${style.width}" 
      height="${style.height}"
    >
      ${htmlIcon}
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

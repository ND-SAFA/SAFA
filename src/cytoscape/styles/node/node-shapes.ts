import { SvgStyle } from "@/types";
import { ARTIFACT_BORDER_WIDTH } from "@/cytoscape/styles/config";

/**
 * Renders an SVG Rectangle.
 *
 * @param style - The node style to render.
 * @param borderColor - The border color.
 * @param bgColor - The background color.
 * @param rx - The border roundness.
 */
export function svgRect(
  style: Pick<SvgStyle, "width" | "height">,
  borderColor: string,
  bgColor: string,
  rx = 0
): string {
  return `
    <rect 
      rx="${rx}" 
      width="${style.width}" 
      height="${style.height}"
      fill="${borderColor}"
      class="artifact-border"
    />
    <rect
      rx="${rx === 0 ? 0 : rx - 1}" 
      x="${ARTIFACT_BORDER_WIDTH}" 
      y="${ARTIFACT_BORDER_WIDTH}" 
      width="${style.width - ARTIFACT_BORDER_WIDTH * 2}" 
      height="${style.height - ARTIFACT_BORDER_WIDTH * 2}"
      fill="${bgColor}"
      class="artifact-svg"
    />
  `;
}

/**
 * Renders an SVG Circle.
 *
 * @param radius - The circle radius to render.
 * @param borderColor - The border color.
 * @param bgColor - The background color.
 */
export function svgCircle(
  radius: number,
  borderColor: string,
  bgColor: string
): string {
  return `
      <circle 
        cx="100" cy="100" r="${radius}"
        fill="${borderColor}"
        class="artifact-border"
      />
      <circle 
        cx="100" cy="100" r="${radius - ARTIFACT_BORDER_WIDTH}"
        fill="${bgColor}"
        class="artifact-svg"
      />
  `;
}

/**
 * Renders an SVG Rhombus.
 *
 * @param style - The node style to render.
 * @param xOffset - The x offset to shift the top of the quadrilateral by.
 * @param borderColor - The border color.
 * @param bgColor - The background color.
 */
export function svgRhombus(
  style: Pick<SvgStyle, "width" | "height">,
  xOffset: number,
  borderColor: string,
  bgColor: string
): string {
  return `
     <polygon 
        points="
          ${xOffset},0 
          ${style.width + xOffset},0 
          ${style.width},${style.height} 
          0,${style.height}"
        fill="${borderColor}"
        class="artifact-border"
      />
      <polygon
        points="
          ${xOffset + ARTIFACT_BORDER_WIDTH},
            ${ARTIFACT_BORDER_WIDTH}
          ${style.width + xOffset - ARTIFACT_BORDER_WIDTH},
            ${ARTIFACT_BORDER_WIDTH}
          ${style.width - ARTIFACT_BORDER_WIDTH},
            ${style.height - ARTIFACT_BORDER_WIDTH} 
          ${ARTIFACT_BORDER_WIDTH},
            ${style.height - ARTIFACT_BORDER_WIDTH}"
        fill="${bgColor}"
        class="artifact-svg"
      />
  `;
}

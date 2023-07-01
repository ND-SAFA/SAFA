import { SvgStyle } from "@/types";
import { ARTIFACT_BORDER_WIDTH } from "@/cytoscape/styles/config";

/**
 * Renders an SVG Rectangle.
 *
 * @param style - The node style to render.
 * @param rx - The border roundness.
 */
export function svgRect(
  style: Pick<SvgStyle, "width" | "height" | "color">,
  rx = 0
): string {
  // const bar = barColor
  //   ? //   ? `
  //     //  <clipPath id="node-click-path">
  //     //     <rect
  //     //       rx="${rx - 1}"
  //     //       width="${style.width}"
  //     //       height="${style.height}"
  //     //     />
  //     //   </clipPath>
  //     //   <rect
  //     //     style="clip-path: url(#node-click-path);"
  //     //     width="9"
  //     //     height="100%"
  //     //     fill="${barColor}"
  //     //   />
  //     // `
  //     `
  //       <rect
  //         rx="2"
  //         width="4"
  //         height="${style.height - 12}"
  //         y="6"
  //         x="6"
  //         fill="${barColor}"
  //       />
  //   `
  //   : "";

  return `
    <rect 
      rx="${rx}" 
      width="${style.width}" 
      height="${style.height}"
      class="artifact-border"
      fill="${style.color}"
    />
    <rect
      rx="${rx === 0 ? 0 : rx - 1}" 
      x="${ARTIFACT_BORDER_WIDTH}" 
      y="${ARTIFACT_BORDER_WIDTH}" 
      width="${style.width - ARTIFACT_BORDER_WIDTH * 2}" 
      height="${style.height - ARTIFACT_BORDER_WIDTH * 2}"
      class="artifact-svg"
    />
  `;
}

/**
 * Renders an SVG Circle.
 *
 * @param radius - The circle radius to render.
 */
export function svgCircle(radius: number): string {
  return `
      <circle 
        cx="100" cy="100" r="${radius}"
        class="artifact-border"
      />
      <circle 
        cx="100" cy="100" r="${radius - ARTIFACT_BORDER_WIDTH}"
        class="artifact-svg"
      />
  `;
}

/**
 * Renders an SVG Rhombus.
 *
 * @param style - The node style to render.
 * @param xOffset - The x offset to shift the top of the quadrilateral by.
 */
export function svgRhombus(
  style: Pick<SvgStyle, "width" | "height">,
  xOffset: number
): string {
  return `
     <polygon 
        points="
          ${xOffset},0 
          ${style.width + xOffset},0 
          ${style.width},${style.height} 
          0,${style.height}"
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
        class="artifact-svg"
      />
  `;
}

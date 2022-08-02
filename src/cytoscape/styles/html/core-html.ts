import { capitalize } from "@/util";
import { getBody } from "./artifact-helper";

/**
 * Creates the HTML for representing a node's header.
 *
 * @param title - The title to render.
 *
 * @return stringified HTML for the node.
 */
export function htmlHeader(title: string): string {
  return `
    <strong 
      class="artifact-header text-body-1" 
      style="height: 28px; font-weight: 600"
    >
      ${capitalize(title)}
    </strong>
  `;
}

/**
 * Creates the HTML for representing an artifact's subheader.
 *
 * @param subtitle - The subtitle to render.
 *
 * @return stringified HTML for the node.
 */
export function htmlSubheader(subtitle: string): string {
  return `
    <strong 
      class="artifact-sub-header text-body-1" 
      style="height: 28px; font-weight: 600"
    >
      ${subtitle}
    </strong>
  `;
}

/**
 * Creates the HTML for representing an artifact's body.
 *
 * @param body - The text body to render.
 * @param truncateLength - The max body length.
 * @param height - The height in pixes of the container.
 * @param width - The width in pixes of the container.
 *
 * @return stringified HTML for the node.
 */
export function htmlBody(
  body: string,
  truncateLength: number,
  width?: number,
  height?: number
): string {
  const nodeWidth = width ? `width: ${width}px;` : "";
  const nodeHeight = width ? `height: ${height}px;` : "";

  return `
    <span class="text-body-2 artifact-body" style="${nodeWidth}${nodeHeight}">
      ${getBody(body, truncateLength)}
    </span>
  `;
}

/**
 * Creates the HTML for representing an artifact.
 *
 * @param elements - The elements to render within the container.
 * @param height - The height in pixes of the container.
 * @param width - The width in pixes of the container.
 * @param opacity - The opacity of the container.
 * @param color - The background color of the container.
 *
 * @return stringified HTML for the node.
 */
export function htmlContainer(
  elements: string[],
  {
    width,
    height,
    opacity,
    color,
  }: {
    width?: number;
    height?: number;
    opacity?: number;
    color?: string;
  } = {}
): string {
  const backgroundColor = color ? `background-color: ${color};` : "";
  const visibility = opacity !== undefined ? `opacity: ${opacity};` : "";
  const nodeWidth = width ? `width: ${width}px;` : "";
  const nodeHeight = height ? `height: ${height}px;` : "";
  const classes =
    width && height
      ? "artifact-container artifact-border"
      : "artifact-container";

  return `
    <div 
      class="${classes}"
      style="${nodeWidth}${nodeHeight}${backgroundColor}${visibility}"
    >
      ${elements.join("\n")}
    </div>
  `;
}

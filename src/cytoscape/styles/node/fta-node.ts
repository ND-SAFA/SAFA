import { ArtifactCytoElementData } from "@/types";

/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
export function htmlFTA(data: ArtifactCytoElementData): string {
  const visibility =
    data.opacity !== undefined ? `opacity: ${data.opacity};` : "";

  return `
    <div style="${visibility};">
      <strong class="text-h5">${data.logicType}</strong>
    </div>
  `;
}

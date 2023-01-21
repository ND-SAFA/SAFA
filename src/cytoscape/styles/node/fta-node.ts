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
      <strong class="text-h5" style="font-weight: 600">${data.logicType}</strong>
    </div>
  `;
}

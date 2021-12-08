import { HtmlDefinition } from "@/types";
import { TimNodeData } from "@/types/components/tim-tree";
import { TIM_NODE_HEIGHT, TIM_NODE_WIDTH } from "@/cytoscape";

export const timNodeHtml: HtmlDefinition<TimNodeData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data?: TimNodeData) {
    // This handles an issue with ghost nodes that are not typesafe.
    if (!data) return "";

    return createTimNodeHtml(data);
  },
};

/**
 * Creates the HTML for displaying nodes with in the TIM tree.
 * @param data The TIM's node data.
 */
function createTimNodeHtml(data: TimNodeData): string {
  const elements: string[] = [
    `<span class="text-h6 artifact-header" style="white-space: normal">${data.id}</span>`,
    `<span class="text-center text-body-1" >${data.count}</span>`,
  ];

  return wrapInColumnContainer(data, elements);
}

/**
 * Creates a div surrounding all of the given html laid out in columns order.
 *
 * @param data - The data for the current node.
 * @param elements - The elements to render within the node.
 */
function wrapInColumnContainer(data: TimNodeData, elements: string[]): string {
  return `
  <div 
    class="artifact-container" 
    style="width: ${TIM_NODE_WIDTH}px; height: ${TIM_NODE_HEIGHT}px"
  >
    ${elements.join("")}
  </div>`;
}

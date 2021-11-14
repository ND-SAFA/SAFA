import { HtmlDefinition } from "@/types";
import { TimNodeData } from "@/types/components/tim-tree";

export const timNodeHtml: HtmlDefinition<TimNodeData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data: TimNodeData) {
    return data !== undefined ? createTimNodeHtml(data) : "";
  },
};

/**
 * Creates the HTML for displaying nodes with in the TIM tree.
 * @param data The TIM's node data.
 */
function createTimNodeHtml(data: TimNodeData): string {
  const borderStyle = "border-bottom: 1px solid black";
  const elements: string[] = [
    `<strong class="pa-0 ma-0" style="${borderStyle}">${data.id}</strong>`,
    `<div class="text-center pa-0 ma-0" >${data.count}</div>`,
  ];
  return wrapInColumnContainer(data, elements);
}

/**
 * Creates a div surrounding all of the given html laid out in columns order
 * @param data
 * @param elements
 */
function wrapInColumnContainer(data: TimNodeData, elements: string[]): string {
  return `
  <div style="display: flex;flex-direction: column;">
    ${elements.join("")}
  </div>`;
}

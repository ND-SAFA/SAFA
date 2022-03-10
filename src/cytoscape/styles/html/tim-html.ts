import { HtmlDefinition } from "@/types";
import { TimNodeData } from "@/types/components/tim-tree";
import { TIM_NODE_HEIGHT, TIM_NODE_WIDTH } from "@/cytoscape";
import { htmlContainer } from "@/cytoscape/styles/html/core-html";

/**
 * Defines tim node html.
 */
export const timNodeHtml: HtmlDefinition<TimNodeData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data?: TimNodeData) {
    if (!data) return "";

    return htmlContainer(
      [
        `<span class="text-h6 artifact-header" style="white-space: normal">${data.id}</span>`,
        `<span class="text-center text-body-1" >${data.count}</span>`,
      ],
      { width: TIM_NODE_WIDTH, height: TIM_NODE_HEIGHT }
    );
  },
};

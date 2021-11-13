import { HtmlDefinition } from "@/types";
import { TimNodeData } from "@/types/components/tim-tree";
import {
  TIM_NODE_HEIGHT,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config/tim-tree-config";

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

function createTimNodeHtml(data: TimNodeData): string {
  const height = TIM_NODE_HEIGHT;
  const width = TIM_NODE_WIDTH;
  const elements = [data.id, data.count];
  return wrapInNodeContainer(data, elements, width, height);
}

function wrapInNodeContainer(
  data: TimNodeData,
  elements: any[],
  width: number,
  height: number
): string {
  return `
  <div class="debug" style="width:${width}px;height:${height}px;">
   <p>${elements.join("\n")}</p>
  </div>`;
}

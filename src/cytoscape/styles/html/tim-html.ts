import { HtmlDefinition } from "@/types";
import { ArtifactTypeNodeData } from "@/types/components/tim-tree";
import {
  TIM_NODE_HEIGHT,
  TIM_NODE_WIDTH,
} from "@/cytoscape/styles/config/tim-tree-config";

export const timNodeHtml: HtmlDefinition<ArtifactTypeNodeData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data: ArtifactTypeNodeData) {
    return data !== undefined ? createTimNodeHtml(data) : "";
  },
};

function createTimNodeHtml(data: ArtifactTypeNodeData): string {
  const height = TIM_NODE_HEIGHT;
  const width = TIM_NODE_WIDTH;
  const elements = [data.id, data.count];
  return wrapInNodeContainer(data, elements, width, height);
}

function wrapInNodeContainer(
  data: ArtifactTypeNodeData,
  elements: any[],
  width: number,
  height: number
): string {
  return `
  <div class="debug" style="width:${width}px;height:${height}px;">
   <p>${elements.join("\n")}</p>
  </div>`;
}

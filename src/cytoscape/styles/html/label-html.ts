import { ArtifactData, HtmlDefinition, TimNodeData } from "@/types";
import {
  ARTIFACT_NODE_SELECTOR,
  TIM_NODE_SELECTOR,
} from "@/cytoscape/styles/stylesheets";
import { svgTIM } from "./tim-node";
import { svgDefault } from "./default-node";
import { svgSafetyCase } from "./sc-node";
import { htmlFTA } from "./fta-node";

/**
 * Defines tim node html.
 */
export const timNodeHtml: HtmlDefinition<TimNodeData> = {
  query: TIM_NODE_SELECTOR,
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data?: TimNodeData) {
    if (!data) return "";

    return svgTIM(data);
  },
};

/**
 * Renders artifact html.
 */
export const artifactHtml: HtmlDefinition<ArtifactData> = {
  query: ARTIFACT_NODE_SELECTOR,
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data?: ArtifactData) {
    if (!data?.artifactType) return "";

    if (data.logicType) {
      return htmlFTA(data);
    } else if (data.safetyCaseType) {
      return svgSafetyCase(data);
    } else {
      return svgDefault(data);
    }
  },
};

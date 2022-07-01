import { ArtifactData, HtmlDefinition } from "@/types";
import { getBackgroundColor } from "@/util";
import { htmlContainer, htmlSubheader } from "./core-html";
import { svgSafetyCase, svgDefault } from "./artifact-safety-case";

/**
 * Renders artifact html.
 */
export const artifactHtml: HtmlDefinition<ArtifactData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data?: ArtifactData) {
    if (!data?.artifactType) return "";

    // data.hiddenChildren = 3;
    // data.warnings = [
    //   { ruleMessage: "Warning", ruleName: "Warning" },
    //   { ruleMessage: "Warning", ruleName: "Warning" },
    // ];
    // data.childDeltaStates = [
    //   ArtifactDeltaState.ADDED,
    //   ArtifactDeltaState.MODIFIED,
    //   ArtifactDeltaState.REMOVED,
    // ];

    if (data.logicType) {
      return htmlFTA(data);
    } else if (data.safetyCaseType) {
      return svgSafetyCase(data);
    } else {
      return svgDefault(data);
    }
  },
};

/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlFTA(data: ArtifactData): string {
  return htmlContainer([htmlSubheader(data.logicType || "")], {
    opacity: data.opacity,
    color: getBackgroundColor(data.artifactDeltaState),
  });
}

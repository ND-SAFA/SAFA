import { ArtifactData, HtmlDefinition } from "@/types";
import { ARTIFACT_HEIGHT, ARTIFACT_WIDTH } from "@/cytoscape/styles/config";
import { getBackgroundColor } from "@/util";
import {
  htmlBody,
  htmlContainer,
  htmlHeader,
  htmlSubheader,
} from "./core-html";
import { htmlSafetyCase } from "./safety-case-html";
import { htmlStoplight } from "./artifact-stoplight";
import { getWarningMessage, getWarnings } from "./artifact-helper";

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

    if (data.safetyCaseType) {
      return htmlSafetyCase(data);
    } else if (data.logicType) {
      return htmlFTA(data);
    } else {
      return htmlArtifact(data);
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

/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlArtifact(data: ArtifactData): string {
  const hasFooter = !!(data.warnings?.length || data.hiddenChildren);
  const truncateLength = hasFooter ? 100 : 150;
  const isCode = data.artifactType.toLowerCase().includes("code");

  return htmlContainer(
    [
      htmlHeader(data.artifactType),
      htmlSubheader(data.artifactName),
      htmlBody(isCode ? "" : data.body, truncateLength),
      htmlFooter(data),
      htmlStoplight(data),
    ],
    {
      width: ARTIFACT_WIDTH * 1.95,
      height: ARTIFACT_HEIGHT * 2.7,
      opacity: data.opacity,
      color: getBackgroundColor(data.artifactDeltaState),
    }
  );
}

/**
 * Creates the HTML for representing an artifact node's warning and collapsed children.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlFooter(data: ArtifactData): string {
  const message = getWarningMessage(data);
  const warningCount = getWarnings(data);
  const warning =
    warningCount > 0
      ? `
        <div class="d-flex flex-grow-1 px-1 warning-text text-body-1">
          <span class="material-icons md-18 pr-1">warning</span>
          <span class="artifact-footer-text">(${warningCount}) ${message}</span>
        </div>
      `
      : "";
  const hiddenChildren = data.hiddenChildren
    ? `
      <div class="d-flex flex-grow-1 pr-1 text-body-1">
        <span class="material-icons md-18">expand_more</span>
        <span>
          ${data.hiddenChildren} ${warning ? "" : "Hidden"}
        </span>
      </div>
    `
    : "";

  return `<div class="artifact-footer">${hiddenChildren}${warning}</div>`;
}

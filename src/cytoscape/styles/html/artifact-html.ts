import { ArtifactData, ArtifactDeltaState, HtmlDefinition } from "@/types";
import { ARTIFACT_HEIGHT, ARTIFACT_WIDTH } from "@/cytoscape/styles/config";
import { capitalize, getBackgroundColor, ThemeColors } from "@/util";
import {
  htmlBody,
  htmlContainer,
  htmlHeader,
  htmlSubheader,
} from "./core-html";

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
  const displayChildren = !!data.hiddenChildren;
  let displayWarning = !!data.warnings?.length;
  let message = data.warnings?.[0]?.ruleName || "Warning";
  let warningCount = data.warnings?.length || 0;

  if (displayChildren) {
    displayWarning ||= !!data.childWarnings?.length;
    message = data.childWarnings?.[0]?.ruleName || message;
    warningCount += data.childWarnings?.length || 0;
  }

  const warning = `
    <div class="d-flex flex-grow-1 px-1 warning-text text-body-1">
      <span class="material-icons md-18 pr-1">warning</span>
      <span class="artifact-footer-text">(${warningCount}) ${message}</span>
    </div>
  `;

  const hiddenChildren = `
    <div class="d-flex flex-grow-1 pr-1 text-body-1">
      <span class="material-icons md-18">expand_more</span>
      <span>
        ${data.hiddenChildren} ${displayWarning ? "" : "Hidden"}
      </span>
    </div>
  `;

  return `
    <div class="artifact-footer">
      ${displayChildren ? hiddenChildren : ""}
      ${displayWarning ? warning : ""}
    </div>
  `;
}

/**
 * Creates the HTML for representing an artifact node's child delta states.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlStoplight(data: ArtifactData): string {
  const { childDeltaStates = [] } = data;

  if (!childDeltaStates.length) return "";

  const renderAdded = childDeltaStates.includes(ArtifactDeltaState.ADDED);
  const renderRemoved = childDeltaStates.includes(ArtifactDeltaState.REMOVED);
  const renderMod = childDeltaStates.includes(ArtifactDeltaState.MODIFIED);
  const classes = data.safetyCaseType
    ? "d-flex artifact-sc-stoplight"
    : "d-flex artifact-stoplight";

  return `
    <div class="${classes}">
      ${renderAdded ? "<div class='artifact-added flex-grow-1'></div>" : ""}
      ${renderRemoved ? "<div class='artifact-removed flex-grow-1'></div>" : ""}
      ${renderMod ? "<div class='artifact-modified flex-grow-1'></div>" : ""}
    </div>
  `;
}

// Safety case

/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCase(data: ArtifactData): string {
  const type = capitalize(data.safetyCaseType?.toLowerCase() || "");
  const attrs = {
    opacity: data.opacity,
    color: ThemeColors.artifactDefault,
  };
  const header = [
    htmlHeader(type),
    htmlStoplight(data),
    htmlSafetyCaseDetails(data),
  ];

  switch (data.safetyCaseType) {
    case "GOAL":
      return htmlContainer(
        [...header, htmlBody(data.body, 100, 200, 95)],
        attrs
      );
    case "CONTEXT":
      return htmlContainer(
        [...header, htmlBody(data.body, 100, 200, 100)],
        attrs
      );
    case "SOLUTION":
      // return htmlSafetyCaseSolution(data);
      return htmlContainer([...header, htmlBody(data.body, 40, 140, 60)], {
        ...attrs,
        width: 140,
      });
    case "STRATEGY":
      return htmlContainer(
        [...header, htmlBody(data.body, 80, 175, 90)],
        attrs
      );
    default:
      return "";
  }
}

/**
 * Creates the HTML for representing an artifact node's warning and collapsed children.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCaseDetails(data: ArtifactData): string {
  const displayChildren = !!data.hiddenChildren;
  let displayWarning = !!data.warnings?.length;

  if (displayChildren) {
    displayWarning ||= !!data.childWarnings?.length;
  }

  const warning = `
    <div class="d-flex warning-text text-body-1">
      <span class="material-icons md-18">warning</span>
    </div>
  `;

  const hiddenChildren = `
    <div class="d-flex text-body-1 pr-1">
      <span class="material-icons md-18">expand_more</span>
      <span>
        ${data.hiddenChildren} ${displayWarning ? "" : "Hidden"}
      </span>
    </div>
  `;

  return `
    <div class="artifact-sc-details">
      <span class="text-body-1 flex-grow-1 text-center">
        ${data.artifactName}
      </span>
      ${displayChildren ? hiddenChildren : ""}
      ${displayWarning ? warning : ""}
    </div>
  `;
}

/**
 * Creates the HTML safety case solution.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCaseSolution(data: ArtifactData): string {
  return `
    <div>
      <svg 
        width="200" 
        height="200" 
        style="margin-top: 7px"
      >
        <circle 
          cx="100" cy="100" r="92"
          fill="${ThemeColors.artifactBorder}"
        />
        <circle 
          cx="100" cy="100" r="91"
          fill="${ThemeColors.artifactDefault}"
        />
        <text x="72" y="35" fill="#36405a" >Solution</text>
        <line 
          x1="40" y1="42" x2="160" y2="42" 
          stroke="rgb(136, 136, 136)" 
          shape-rendering="crispEdges"
        />
      </svg>
    </div>
  `;
}

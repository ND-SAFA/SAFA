import { ArtifactData, ArtifactDeltaState, HtmlDefinition } from "@/types";
import {
  ARTIFACT_HEIGHT,
  ARTIFACT_WIDTH,
} from "@/cytoscape/styles/config/artifact-tree-config";
import { capitalize } from "@/util";

const TEST_MODE = false;

export const artifactHtml: HtmlDefinition<ArtifactData> = {
  query: "node",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data: ArtifactData) {
    return createNodeHtml(data);
  },
};

export const nodeWarningHtml: HtmlDefinition<ArtifactData> = {
  query: "node[warnings]",
  halign: "center",
  valign: "center",
  halignBox: "center",
  valignBox: "center",
  tpl(data: ArtifactData) {
    return createNodeHtml(data);
  },
};

/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 * @param widthFactor - The factor to apply to the artifact width.
 * @param heightFactor - The factor to apply to the artifact height.
 *
 * @return stringified HTML for the node.
 */
function createNodeHtml(
  data: ArtifactData,
  widthFactor = 1.95,
  heightFactor = 2.7
): string {
  const height = ARTIFACT_HEIGHT * heightFactor;
  const width = ARTIFACT_WIDTH * widthFactor;
  const bodyFactor = 0.4;

  const elements = [
    createNodeHeader(data, height * 0.2),
    createNodeSubHeader(data, height * 0.15),
    createNodeBody(data, height * bodyFactor),
    createNodeFooter(data),
    createNodeStoplight(data),
  ];

  return wrapInNodeContainer(data, elements, width, height);
}

/**
 * Creates the HTML for representing an artifact node's header.
 *
 * @param data - The artifact data to render.
 * @param height - The height in pixes of the header.
 *
 * @return stringified HTML for the node.
 */
function createNodeHeader(data: ArtifactData, height: number): string {
  return `
    <strong class="artifact-header" style="height:${height}px">
      ${capitalize(data.artifactType)}
    </strong>
  `;
}

/**
 * Creates the HTML for representing an artifact node's subheader.
 *
 * @param data - The artifact data to render.
 * @param height - The height in pixes of the subheader.
 *
 * @return stringified HTML for the node.
 */
function createNodeSubHeader(data: ArtifactData, height: number): string {
  return `
    <span class="artifact-sub-header" style="height:${height}px">
      ${data.id}
    </span>
  `;
}

/**
 * Creates the HTML for representing an artifact node's body.
 *
 * @param data - The artifact data to render.
 * @param height - The height in pixes of the body.
 *
 * @return stringified HTML for the node.
 */
function createNodeBody(data: ArtifactData, height: number): string {
  const hasFooter = !!(data.warnings?.length || data.hiddenChildren);
  const truncateLength = hasFooter ? 90 : 145;

  const body =
    data.body.length > truncateLength
      ? data.body.slice(0, truncateLength) + "..."
      : data.body;

  return `<span class="artifact-body" style="height:${height}px">${body}</span>`;
}

/**
 * Creates the HTML for representing an artifact node's warning and collapsed children.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function createNodeFooter(data: ArtifactData): string {
  if (TEST_MODE) {
    data.hiddenChildren = 3;
    data.warnings = [
      { ruleName: "Very Long Rule Name", ruleMessage: "message" },
    ];
  }

  const displayWarning = !!data.warnings?.length;
  const displayChildren = !!data.hiddenChildren;
  const message = data.warnings?.[0]?.ruleName || "Warning";

  const warning = `
    <div class="d-flex flex-grow-1 px-1 warning-text">
      <span class="material-icons md-18 pr-1">warning</span>
      <span class="artifact-footer-text">${message}</span>
    </div>
  `;

  const hiddenChildren = `
    <div class="d-flex flex-grow-1 pr-1">
      <span class="material-icons md-18">expand_more</span>
      <span>${data.hiddenChildren} ${displayWarning ? "" : "Hidden"}</span>
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
function createNodeStoplight(data: ArtifactData): string {
  if (TEST_MODE) {
    data.childrenDeltaStates = [
      ArtifactDeltaState.ADDED,
      ArtifactDeltaState.REMOVED,
      ArtifactDeltaState.MODIFIED,
    ];
  }

  if (!data.childrenDeltaStates?.length) return "";

  const renderAdded = data.childrenDeltaStates.includes(
    ArtifactDeltaState.ADDED
  );
  const renderRemoved = data.childrenDeltaStates.includes(
    ArtifactDeltaState.REMOVED
  );
  const renderMod = data.childrenDeltaStates.includes(
    ArtifactDeltaState.MODIFIED
  );

  return `
    <div class="d-flex artifact-stoplight">
      ${renderAdded ? "<div class='artifact-added flex-grow-1'></div>" : ""}
      ${renderRemoved ? "<div class='artifact-removed flex-grow-1'></div>" : ""}
      ${renderMod ? "<div class='artifact-modified flex-grow-1'></div>" : ""}
    </div>
  `;
}

/**
 * Creates the HTML for representing an artifact node's container.
 *
 * @param data - The artifact data to render.
 * @param elements - The elements to render within the container.
 * @param height - The height in pixes of the container.
 * @param width - The width in pixes of the container.
 *
 * @return stringified HTML for the node.
 */
function wrapInNodeContainer(
  data: ArtifactData,
  elements: string[],
  width: number,
  height: number
): string {
  return `
    <div 
      class="artifact-container" 
      style="width:${width}px;height:${height}px;opacity:${data.opacity}"
    >
      ${elements.join("\n")}
    </div>
  `;
}

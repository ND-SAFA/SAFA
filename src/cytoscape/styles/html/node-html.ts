import { ArtifactData } from "@/types/domain/artifact";
import { HtmlDefinition } from "@/types/cytoscape/node-html-label";
import {
  ARTIFACT_HEIGHT,
  ARTIFACT_WIDTH,
} from "@/cytoscape/styles/config/artifact";
import { getArtifactTypePrintName } from "@/util/string-helper";
import { TRUNCATE_LENGTH } from "@/cytoscape/styles/config/graph";

export const nodeHtml: HtmlDefinition = {
  query: "node", // cytoscape que./cytoscape-stylesheets
  halign: "center",
  valign: "center",
  halignBox: "center", // title vertical position. Can be 'left',''center, 'right'
  valignBox: "center", // title relative box vertical position. Can be 'top',''center, 'bottom'
  tpl(data: ArtifactData) {
    return data.body !== undefined ? createNodeHtml(data) : "";
  },
};

export const nodeWarningHtml: HtmlDefinition = {
  query: "node[warnings]", // cytoscape query selector
  halign: "center", // title vertical position. Can be 'left',''center, 'right'
  valign: "center", // title vertical position. Can be 'top',''center, 'bottom'
  halignBox: "center", // title vertical position. Can be 'left',''center, 'right'
  valignBox: "center", // title relative box vertical position. Can be 'top',''center, 'bottom'
  tpl(data: ArtifactData) {
    const message =
      data.warnings !== undefined ? data.warnings[0].ruleName : "idk";
    const warningHtml = `
    <div class="artifact-warning" style="height:25px;">
      <span class="material-icons md-18 mr-3">warning</span>
      <span>${message.slice(0, 20)}</span>
    </div>`;
    return createNodeHtml(data, [warningHtml], 1.95, 2.7);
  },
};

function createNodeHtml(
  data: ArtifactData,
  additionalElements: string[] = [],
  widthFactor = 1.95,
  heightFactor = 2.7
): string {
  const height = ARTIFACT_HEIGHT * heightFactor;
  const width = ARTIFACT_WIDTH * widthFactor;
  const bodyFactor = additionalElements.length === 0 ? 0.75 : 0.5;
  const elements = [
    createNodeHeader(data, height * 0.2),
    createNodeSubHeader(data, height * 0.15),
    createNodeBody(data, height * bodyFactor),
  ].concat(additionalElements);
  return wrapInNodeContainer(data, elements, width, height);
}

function createNodeHeader(data: ArtifactData, height: number): string {
  return `
  <strong class="artifact-header" style="height:${height}px">
  ${getArtifactTypePrintName(data.artifactType)}
  </strong>`;
}

function createNodeSubHeader(data: ArtifactData, height: number): string {
  return `
  <span class="artifact-sub-header" style="height:${height}px">
  ${data.id}
  </span>`;
}

function createNodeBody(data: ArtifactData, height: number): string {
  const body =
    data.body.length > TRUNCATE_LENGTH
      ? data.body.slice(0, TRUNCATE_LENGTH) + "..."
      : data.body;
  return `<span class="artifact-body" style="height:${height}px">${body}</span>`;
}

function wrapInNodeContainer(
  data: ArtifactData,
  elements: string[],
  width: number,
  height: number
): string {
  return `
  <div class="artifact-container" style="width:${width}px;height:${height}px;opacity:${
    data.opacity
  }">
    ${elements.join("\n")}
  </div>`;
}

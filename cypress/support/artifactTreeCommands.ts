import { DataCy, validUser } from "@/fixtures";

Cypress.Commands.add("getNode", (name) => {
  return cy.get(`[data-cy-name="${name}"]`);
});

Cypress.Commands.add("getNodes", (selected) => {
  if (selected) {
    return cy.getCy(DataCy.treeSelectedNode);
  } else {
    return cy
      .getCy(DataCy.treeNode, undefined, 10000)
      .should("be.visible")
      .filter(":visible");
  }
});

Cypress.Commands.add("waitForProjectLoad", (waitForNodes = true) => {
  cy.getCy(DataCy.appLoading).should("not.be.visible");

  if (waitForNodes) {
    cy.getNodes().should("be.visible");
  }
});

Cypress.Commands.add("centerGraph", () => {
  // Wait for graph to center.
  cy.clickButton(DataCy.navGraphCenterButton).wait(200);
});

Cypress.Commands.add("selectArtifact", (name) => {
  cy.inputText(DataCy.artifactSearchNavInput, name).clickButton(
    DataCy.artifactSearchItem,
    "first"
  );
});

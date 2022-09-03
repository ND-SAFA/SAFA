import { DataCy } from "../fixtures";
import { validUser } from "../fixtures/data/user.json";

Cypress.Commands.add("getNode", (name) => {
  return cy.get(`[data-cy-name="${name}"]`);
});

Cypress.Commands.add("getNodes", (selected) => {
  if (selected) {
    return cy.getCy(DataCy.treeSelectedNode);
  } else {
    return cy.getCy(DataCy.treeNode, undefined, 10000).filter(":visible");
  }
});

Cypress.Commands.add("waitForProjectLoad", () => {
  cy.getCy(DataCy.appLoading).should("not.be.visible");
});

Cypress.Commands.add("loadCurrentProject", () => {
  cy.visit("/project")
    .login(validUser.email, validUser.password)
    .location("pathname", { timeout: 5000 })
    .should("equal", "/project");

  cy.waitForProjectLoad();
});

Cypress.Commands.add("centerGraph", () => {
  // Wait for graph to center.
  cy.clickButton(DataCy.navGraphCenterButton).wait(200);
});

Cypress.Commands.add("selectArtifact", (name, selectType = "nav") => {
  if (selectType === "nav") {
    cy.inputText(DataCy.artifactSearchNavInput, name).clickButton(
      DataCy.artifactSearchItem,
      "first"
    );
  } else {
    cy.clickButton(DataCy.navToggleRightPanel)
      .inputText(DataCy.artifactSearchSideInput, "F21")
      .clickButton(DataCy.artifactSearchItem, "first");
  }
});

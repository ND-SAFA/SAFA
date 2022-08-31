import { DataCy } from "../fixtures";
import { validUser } from "../fixtures/data/user.json";

Cypress.Commands.add("getNodes", (selected) => {
  if (selected) {
    return cy.getCy(DataCy.treeSelectedNode);
  } else {
    return cy.getCy(DataCy.treeNode, undefined, 10000).filter(":visible");
  }
});

Cypress.Commands.add("loadCurrentProject", () => {
  cy.visit("/project")
    .login(validUser.email, validUser.password)
    .location("pathname", { timeout: 5000 })
    .should("equal", "/project");

  cy.getCy(DataCy.appLoading)
    .should("not.be.visible")
    .getNodes()
    .should("be.visible");
});

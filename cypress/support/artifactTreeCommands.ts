import { DataCy } from "../fixtures";

Cypress.Commands.add("getNodes", (selected) => {
  if (selected) {
    return cy.getCy(DataCy.treeSelectedNode);
  } else {
    return cy.getCy(DataCy.treeNode, undefined, 10000).filter(":visible");
  }
});
